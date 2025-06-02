import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file (create this file with your credentials)
load_dotenv()

def generate_behavior_report(student_name, behavior_data, output_path):
    """
    Generates a PDF report summarizing the behavior of a student.

    :param student_name: str, name or ID of the student
    :param behavior_data: dict, keys are behavior names, values are counts or durations
    :param output_path: str, where to save the PDF file
    :return: output_path
    """
    try:
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, height - 50, f"Behavior Report: {student_name}")

        # Date
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Report Content
        c.setFont("Helvetica", 14)
        y = height - 120
        for behavior, value in behavior_data.items():
            c.drawString(50, y, f"{behavior}: {value}")
            y -= 25

        c.save()
        print(f"PDF report generated successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error generating PDF report: {e}")
        return None

def send_whatsapp_report(twilio_sid, twilio_auth_token, from_whatsapp, to_whatsapp, message_body, media_url=None):
    """
    Sends a WhatsApp message with optional media via Twilio.

    :param twilio_sid: str, Twilio Account SID
    :param twilio_auth_token: str, Twilio Auth Token
    :param from_whatsapp: str, sender WhatsApp number with 'whatsapp:' prefix
    :param to_whatsapp: str, recipient WhatsApp number with 'whatsapp:' prefix
    :param message_body: str, text message to send
    :param media_url: str or None, public URL of the media (PDF) to send, if any
    :return: message SID or None
    """
    try:
        client = Client(twilio_sid, twilio_auth_token)

        message_data = {
            'from_': from_whatsapp,
            'to': to_whatsapp,
            'body': message_body,
        }

        if media_url:
            message_data['media_url'] = [media_url]

        message = client.messages.create(**message_data)
        print(f"WhatsApp message sent successfully. SID: {message.sid}")
        return message.sid
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
        return None

if __name__ == "__main__":
    # Example student behavior data
    student = "Student_001"
    behavior_summary = {
        "Sleep Detections": 3,
        "Phone Usage Duration (minutes)": 15,
        "Eating Instances": 2,
        "Engagement Level (%)": 78
    }

    output_file = "student_001_behavior_report.pdf"

    # Generate PDF report
    report_path = generate_behavior_report(student, behavior_summary, output_file)

    if report_path:
        # Load Twilio credentials from environment variables
        TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
        TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
        FROM_WHATSAPP = os.getenv("TWILIO_PHONE_NUMBER")  # Must be like 'whatsapp:+14155238886'
        TO_WHATSAPP = os.getenv("RECIPIENT_PHONE_NUMBER")  # Must be like 'whatsapp:+917794026640'

        # IMPORTANT:
        # Twilio requires media files to be publicly accessible via URL
        # You cannot send local file paths directly
        # Upload your PDF report to a public URL and set it here:
        PUBLIC_PDF_URL = os.getenv("PUBLIC_PDF_URL")  # e.g. https://yourdomain.com/path/to/report.pdf

        message_body = f"Hello {student}, here is your behavior report."

        # Send WhatsApp message with or without PDF (if you don't have a public URL, send only text)
        send_whatsapp_report(
            TWILIO_SID,
            TWILIO_AUTH_TOKEN,
            FROM_WHATSAPP,
            TO_WHATSAPP,
            message_body,
            media_url=PUBLIC_PDF_URL if PUBLIC_PDF_URL else None
        )
    else:
        print("Report generation failed, skipping WhatsApp message.")
