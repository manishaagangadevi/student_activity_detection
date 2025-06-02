from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
from twilio.rest import Client

def generate_behavior_report(student_name, behavior_data, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 50, f"Behavior Report: {student_name}")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.setFont("Helvetica", 14)
    y = height - 120
    for behavior, value in behavior_data.items():
        c.drawString(50, y, f"{behavior}: {value}")
        y -= 25

    c.save()
    return output_path

def send_whatsapp_message(twilio_sid, twilio_auth_token, from_whatsapp, to_whatsapp, message_body):
    client = Client(twilio_sid, twilio_auth_token)
    message = client.messages.create(
        from_=from_whatsapp,
        to=to_whatsapp,
        body=message_body
    )
    return message.sid

if __name__ == "__main__":
    student = "Student_001"
    behavior_summary = {
        "Sleep Detections": 3,
        "Phone Usage Duration (minutes)": 15,
        "Eating Instances": 2,
        "Engagement Level (%)": 78
    }
    output_file = "student_001_behavior_report.pdf"

    # Generate PDF report locally (for your records)
    generate_behavior_report(student, behavior_summary, output_file)
    print(f"Report saved to {output_file}")

    # Twilio WhatsApp credentials and numbers
    TWILIO_SID = "TWILIO_ACCOUNT_SID"
    TWILIO_AUTH_TOKEN = "TWILIO_AUTH_TOKEN"
    FROM_WHATSAPP = "TWILIO_PHONE_NUMBER"  # Twilio sandbox WhatsApp number
    TO_WHATSAPP = "RECIPIENT_PHONE_NUMBER"   # Your WhatsApp number with country code

    # Compose simple message (without PDF)
    message_body = f"Hello {student}, your behavior report is ready. Please check your email or portal for details."

    try:
        sid = send_whatsapp_message(TWILIO_SID, TWILIO_AUTH_TOKEN, FROM_WHATSAPP, TO_WHATSAPP, message_body)
        print(f"WhatsApp message sent successfully. SID: {sid}")
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
