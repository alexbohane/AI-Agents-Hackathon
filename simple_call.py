from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch from environment
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
from_number = os.getenv("FROM_NUMBER")
to_number = os.getenv("TO_NUMBER")

# Create Twilio client
client = Client(account_sid, auth_token)

# Make the call
try:
    call = client.calls.create(
        to=to_number,
        from_=from_number,
        twiml="""
            <Response>
                <Say voice='man'>Hello, I'm calling on behalf of Elon Musk. We would like to book a table tonight for two people at 8pm this evening, preferably on a table inside if available. Could you please confirm availability?</Say>
            </Response>
        """
    )
    print(f"✅ Appel lancé. SID: {call.sid}")
except Exception as e:
    print(f"❌ Erreur lors de l'appel : {e}")
