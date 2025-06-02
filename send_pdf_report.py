
from twilio.rest import Client
import config

# Add 'whatsapp:' prefix to phone numbers
FROM_WHATSAPP = f'whatsapp:{config.TWILIO_PHONE_NUMBER}'
TO_WHATSAPP = f'whatsapp:{config.RECIPIENT_PHONE_NUMBER}'

# Initialize Twilio client
client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

# Replace this with the actual URL of your PDF
pdf_url = 'https://example.com/path/to/report.pdf'

try:
    message = client.messages.create(
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP,
        media_url=[pdf_url]
    )
    print("✅ PDF report sent:", message.sid)
except Exception as e:
    print("❌ Failed to send PDF report:", e)
