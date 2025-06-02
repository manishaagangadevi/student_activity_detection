import cv2
import mediapipe as mp
import numpy as np
import time
import os
from datetime import datetime
from ultralytics import YOLO
from notifier import send_alert, handle_full_report
import notifier  # Your notifier.py module
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use env vars for notifier
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
RECIPIENT_PHONE_NUMBER = os.getenv("RECIPIENT_PHONE_NUMBER")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Initialize YOLO model (make sure yolov8n.pt is in your directory)
model = YOLO("yolov8n.pt")

# Mediapipe face mesh and hands init
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_hands = mp.solutions.hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

def is_sleeping(face_landmarks):
    # Simple eye openness ratio detection
    left_eye_top = face_landmarks.landmark[159]
    left_eye_bottom = face_landmarks.landmark[145]
    eye_open = abs(left_eye_top.y - left_eye_bottom.y)
    return eye_open < 0.004  # Adjust threshold if needed

def get_behavior(results_face, results_hands, yolo_results):
    # Sleep detection
    if results_face.multi_face_landmarks:
        for face_landmarks in results_face.multi_face_landmarks:
            if is_sleeping(face_landmarks):
                return "Sleeping"

    # YOLO detections for phone or eating
    if yolo_results:
        for result in yolo_results:
            for cls_id in result.boxes.cls.cpu().numpy():
                cls_name = model.names[int(cls_id)]
                if cls_name == "cell phone":
                    return "Using Phone"
                elif cls_name in ["banana", "apple", "orange", "sandwich"]:
                    return "Eating"

    # Hands near mouth (for eating)
    if results_hands.multi_hand_landmarks and results_face.multi_face_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            for face_landmarks in results_face.multi_face_landmarks:
                hand_y = hand_landmarks.landmark[8].y  # index finger tip
                mouth_y = face_landmarks.landmark[13].y  # approximate mouth
                if abs(hand_y - mouth_y) < 0.05:
                    return "Eating"

    return "Normal"

detected_events = []
last_behavior = None
alert_interval = 60  # seconds
last_alert_time = {}

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get detections
    results_yolo = model(frame, verbose=False)
    results_face = mp_face_mesh.process(frame_rgb)
    results_hands = mp_hands.process(frame_rgb)

    behavior = get_behavior(results_face, results_hands, results_yolo)

    # Only alert if behavior changed and not spamming alerts
    current_time = time.time()
    if behavior != "Normal" and behavior != last_behavior:
        if behavior not in last_alert_time or (current_time - last_alert_time
        [behavior] > alert_interval):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            detected_events.append({"time": timestamp, "behavior": behavior})
            last_behavior = behavior
            last_alert_time[behavior] = current_time

            with open("behavior_log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"{timestamp}: {behavior}\n")

            # Send alert using notifier module
            notifier.send_alert(
                student_name="Student 1",
                behavior=behavior,
                timestamp=timestamp,
                twilio_sid=TWILIO_ACCOUNT_SID,
                twilio_token=TWILIO_AUTH_TOKEN,
                twilio_from=TWILIO_PHONE_NUMBER,
                twilio_to=RECIPIENT_PHONE_NUMBER,
                sender_email=SENDER_EMAIL,
                sender_password=SENDER_PASSWORD,
                receiver_email=RECEIVER_EMAIL,
            )

    # Show behavior on frame using YOLO annotated frame
    annotated_frame = results_yolo[0].plot()
    cv2.putText(annotated_frame, f"Behavior: {behavior}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("AI Student Monitoring", annotated_frame)

    # Quit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        notifier.handle_full_report("Student 1", detected_events)  # Send full session report
        break

cap.release()
cv2.destroyAllWindows()
