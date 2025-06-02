# AI-Powered Student Behavior Monitoring System

This project is an AI-based solution that automatically monitors student behavior in smart classrooms using computer vision technologies like YOLOv8 and MediaPipe. It detects activities such as sleeping, using mobile phones, inattentiveness, and sends real-time alerts to faculty via WhatsApp and Email with PDF reports.

**GitHub Repo:** [student_activity_detection](https://github.com/manishaagangadevi/student_activity_detection.git)

## Features

- Real-time activity detection using webcam or CCTV feed
- Behavior classification using YOLOv8 and MediaPipe
- Automatic WhatsApp and Email alerts using Twilio and SMTP
- PDF report generation using FPDF
- Easy integration with smart classroom setups

---

## Technologies Used

- **YOLOv8** – Object detection for mobile usage & inattentiveness
- **MediaPipe** – Pose and hand detection for behavior recognition
- **OpenCV** – Real-time video processing
- **Twilio API** – WhatsApp messaging service
- **smtplib & email.mime** – Email sending with PDF attachments
- **FPDF** – PDF report generation
- **dotenv** – Secure environment variable loading
- **Python (3.10+)**
- **venv** – Virtual environment for dependency isolation


## How It Works

1. Captures real-time student activity through webcam or CCTV.
2. YOLOv8 identifies mobile usage or distractions.
3. MediaPipe tracks posture/pose to detect sleeping/inattentiveness.
4. When a behavior is flagged, it's logged.
5. A PDF report is auto-generated and alerts are sent via WhatsApp and Email.


## Installation

1. Clone the repository:
   git clone https://github.com/manishaagangadevi/student_activity_detection.git
   cd student_activity_detection
   
2.Create and activate virtual environment:
python -m venv venv
venv\Scripts\activate  # On Windows

3.Install dependencies:
pip install -r requirements.txt

4.Create a .env file:
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
RECIPIENT_PHONE_NUMBER=whatsapp:+91xxxxxxxxxx
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECEIVER_EMAIL=faculty_email@example.com


