import os
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from twilio.rest import Client
from dotenv import load_dotenv
from fpdf import FPDF

load_dotenv()

# Load environment variables
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
recipient_phone = os.getenv("RECIPIENT_PHONE_NUMBER")
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")

# Send WhatsApp Alert
def send_whatsapp_alert(message):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_=twilio_phone,
            body=message,
            to=recipient_phone
        )
        print(f"WhatsApp alert sent: SID {message.sid}")
    except Exception as e:
        print(f"Failed to send WhatsApp alert: {e}")

# Generate PDF Report
def generate_pdf_report(student_name, behaviors):
    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    filename = f"{student_name}_Report_{date_str}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.set_text_color(0, 0, 0)

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Behavior Report for {student_name}", ln=True, align='C')
    pdf.ln(10)

    # Date and Time
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Date: {date_str}", ln=True)

    # Behavior Table
    pdf.ln(5)
    for behavior in behaviors:
        pdf.cell(200, 10, f"{behavior['time']}: {behavior['behavior']}", ln=True)

    pdf.output(filename)
    return filename

# Send Email Alert with PDF Attachment
def send_email_report(student_name, behaviors):
    try:
        now = datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        subject = f"[Alert] Student Behavior Report – {student_name} – {time_str}"

        body = (
            f"Hello,\n\n"
            f"Please find attached the detailed behavior report for {student_name}.\n\n"
            f"Regards,\nAI Monitoring System"
        )

        # Create PDF and get filename
        pdf_filename = generate_pdf_report(student_name, behaviors)

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        # Add text body
        msg.attach(MIMEText(body, "plain"))

        # Attach PDF file
        with open(pdf_filename, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(pdf_filename))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_filename)}"'
            msg.attach(part)

        # Email sending
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print(f"Email with PDF report sent to {receiver_email}")

        # Optional: delete the PDF after sending
        os.remove(pdf_filename)

    except Exception as e:
        print(f"Failed to send email alert: {e}")
        print("Email credentials missing or invalid.")

# MAIN function to be called from main.py
def send_alert(student_name, behavior, timestamp, **kwargs):
    message = f" {student_name} is {behavior} at {timestamp}."
    send_whatsapp_alert(message)

def handle_full_report(student_name, detected_events):
    send_email_report(student_name, detected_events)
