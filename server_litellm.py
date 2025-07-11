from fastapi import FastAPI, WebSocket
from typing import Dict, List, Optional
import json
from litellm import acompletion
from dotenv import load_dotenv
import uvicorn
from prompt_config import system_prompt

# Load environment variables
load_dotenv()
app = FastAPI()
sessions: Dict[str, List[dict]] = {}

# import litellm
# litellm._turn_on_debug()
system_prompt = system_prompt

async def draft_response(model, messages):
    response = await acompletion(model=model, messages=messages, stream=True)
    async for part in response:
        if part.choices[0].delta.content is not None:
            # print(part.choices[0].delta.content)
            yield {
                "token": part.choices[0].delta.content,
                "last": False,
                "type": "text",
            }

    yield {
        "token": "",
        "type": "text",
        "last": True,
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    call_sid: Optional[str] = None

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            # print("Message type: ", message["type"])
            print("ConvRelay Message: ", message)

            if message["type"] == "setup":
                call_sid = message["callSid"]
                print(f"Setup initiated for call {call_sid} from **{message['from'][-4:]}")


                # Initialize conversation history and system prompt
                sessions[str(call_sid)] = [
                    {"role": "system", "content": system_prompt}
                ]

            elif message["type"] == "prompt":
                prompt = message["voicePrompt"]
                print("Prompt: ", prompt)

                # Retrieve and update conversation history
                # Make sure call_sid is not None
                conversation = sessions[str(call_sid)] if call_sid is not None else []
                conversation.append({"role": "user", "content": prompt})

                # print(conversation)

                response = ""
                claude = "anthropic/claude-3-7-sonnet-20250219"

                async for event in draft_response(claude, messages=conversation):
                    await websocket.send_json(event)
                    response += event["token"]

                #save back
                print("AI response: ", response)
                conversation.append({"role": "assistant", "content": response})
                sessions[str(call_sid)] = conversation

            elif message["type"] == "interrupt":
                print("Response interrupted")

            elif message["type"] == "error":
                print("Error")

            else:
                print("Unknown message type")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if call_sid:
            sessions.pop(call_sid, None)
        print("Client has disconnected.")

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8080)
