import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

def detect_behavior(frame):
    behavior = "Normal"
    with mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1) as face_mesh, \
         mp_hands.Hands(static_image_mode=False, max_num_hands=2) as hands:

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_results = face_mesh.process(image_rgb)
        hand_results = hands.process(image_rgb)

        # Sleep Detection: Based on eye openness
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                # Eye landmark indices (left and right eye)
                left_eye = [33, 160, 158, 133]
                right_eye = [362, 385, 387, 263]
                def eye_aspect_ratio(eye_points):
                    a = np.linalg.norm(np.array([face_landmarks.landmark[eye_points[1]].x,
                                                 face_landmarks.landmark[eye_points[1]].y]) -
                                       np.array([face_landmarks.landmark[eye_points[2]].x,
                                                 face_landmarks.landmark[eye_points[2]].y]))
                    b = np.linalg.norm(np.array([face_landmarks.landmark[eye_points[0]].x,
                                                 face_landmarks.landmark[eye_points[0]].y]) -
                                       np.array([face_landmarks.landmark[eye_points[3]].x,
                                                 face_landmarks.landmark[eye_points[3]].y]))
                    return a / b

                left_ear = eye_aspect_ratio(left_eye)
                right_ear = eye_aspect_ratio(right_eye)

                if left_ear < 0.2 and right_ear < 0.2:
                    behavior = "Sleeping "

        # Mobile/Eating Detection: Hands near face
        if hand_results.multi_hand_landmarks and face_results.multi_face_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                for face_landmarks in face_results.multi_face_landmarks:
                    hand = hand_landmarks.landmark[9]  # Middle of palm
                    face = face_landmarks.landmark[1]  # Nose tip
                    dist = np.linalg.norm(np.array([hand.x, hand.y]) - np.array([face.x, face.y]))
                    if dist < 0.1:
                        if behavior != "Sleeping ":
                            behavior = "Phone/Eating"
    return behavior
