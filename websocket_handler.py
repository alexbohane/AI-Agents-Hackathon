from fastapi import WebSocket
from typing import Dict, List, Optional
import json
from prompt_config import system_prompt
from agent_langgraph import run_agent

sessions: Dict[str, List[dict]] = {}

async def handle_websocket(websocket: WebSocket):
    await websocket.accept()
    call_sid: Optional[str] = None

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "setup":
                call_sid = message["callSid"]
                sessions[str(call_sid)] = [
                    {"role": "system", "content": system_prompt}
                ]

            elif message["type"] == "prompt":
                prompt = message["voicePrompt"]
                conversation = sessions.get(str(call_sid), [])
                conversation.append({"role": "user", "content": prompt})

                ai_response = await run_agent(conversation)

                # Stream as single message for now
                await websocket.send_json({
                    "token": ai_response,
                    "last": True,
                    "type": "text"
                })

                conversation.append({"role": "assistant", "content": ai_response})
                sessions[str(call_sid)] = conversation

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if call_sid:
            sessions.pop(call_sid, None)
