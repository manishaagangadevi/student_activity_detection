import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
RECIPIENT_PHONE_NUMBER = os.getenv("RECIPIENT_PHONE_NUMBER")

print("Loaded phone numbers:")
print(TWILIO_PHONE_NUMBER)
print(RECIPIENT_PHONE_NUMBER)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

try:
    message = client.messages.create(
        body="Hello from Twilio WhatsApp!",
        from_=TWILIO_PHONE_NUMBER,
        to=RECIPIENT_PHONE_NUMBER
    )
    print("Message sent! SID:", message.sid)
except Exception as e:
    print("Error sending message:", e)
