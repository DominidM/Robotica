#captura de pantalla a la camara
import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import os
import csv
from datetime import datetime

# Parámetros
RESOLUTION = (640, 480)
GESTURES = {
    'Bien': lambda lms: lms['thumb_tip'][1] < lms['thumb_pip'][1] and all(lms[f'{finger}_tip'][1] > lms['thumb_pip'][1] for finger in ['index_finger', 'middle_finger', 'ring_finger', 'pinky']),
    'Mal': lambda lms: lms['thumb_tip'][1] > lms['thumb_pip'][1] and all(lms[f'{finger}_tip'][1] < lms['thumb_pip'][1] for finger in ['index_finger', 'middle_finger', 'ring_finger', 'pinky']),
    'Hola': lambda lms, history: len(history) >= 8 and max([pos[0] for pos in history]) - min([pos[0] for pos in history]) > 80
}
hand_positions = deque(maxlen=8)

# Preparar directorios
output_images = "dataset/images"
output_landmarks = "dataset/landmarks"
os.makedirs(output_images, exist_ok=True)
os.makedirs(output_landmarks, exist_ok=True)

def distancia_euclidiana(p1, p2):
    return ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2) ** 0.5

def extract_landmarks(hand_landmarks, image_width, image_height):
    return {
        'thumb_tip': (int(hand_landmarks.landmark[4].x * image_width), int(hand_landmarks.landmark[4].y * image_height)),
        'thumb_pip': (int(hand_landmarks.landmark[2].x * image_width), int(hand_landmarks.landmark[2].y * image_height)),
        'index_finger_tip': (int(hand_landmarks.landmark[8].x * image_width), int(hand_landmarks.landmark[8].y * image_height)),
        'index_finger_pip': (int(hand_landmarks.landmark[6].x * image_width), int(hand_landmarks.landmark[6].y * image_height)),
        'middle_finger_tip': (int(hand_landmarks.landmark[12].x * image_width), int(hand_landmarks.landmark[12].y * image_height)),
        'middle_finger_pip': (int(hand_landmarks.landmark[10].x * image_width), int(hand_landmarks.landmark[10].y * image_height)),
        'ring_finger_tip': (int(hand_landmarks.landmark[16].x * image_width), int(hand_landmarks.landmark[16].y * image_height)),
        'ring_finger_pip': (int(hand_landmarks.landmark[14].x * image_width), int(hand_landmarks.landmark[14].y * image_height)),
        'pinky_tip': (int(hand_landmarks.landmark[20].x * image_width), int(hand_landmarks.landmark[20].y * image_height)),
        'pinky_pip': (int(hand_landmarks.landmark[18].x * image_width), int(hand_landmarks.landmark[18].y * image_height)),
        'wrist': (int(hand_landmarks.landmark[0].x * image_width), int(hand_landmarks.landmark[0].y * image_height))
    }

def save_data(image, results, timestamp):
    img_path = f"{output_images}/{timestamp}.jpg"
    cv2.imwrite(img_path, image)
    csv_path = f"{output_landmarks}/{timestamp}.csv"
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["hand", "landmark_index", "x", "y", "z"])
        if results.multi_hand_landmarks:
            for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
                for lm_index, lm in enumerate(hand_landmarks.landmark):
                    writer.writerow([hand_index, lm_index, lm.x, lm.y, lm.z])
    print(f" Imagen y landmarks guardados: {timestamp}")

def recognize_gesture(lms, history):
    for gesture, rule in GESTURES.items():
        if gesture == "Hola":
            if rule(lms, history):
                return gesture
        else:
            if rule(lms):
                return gesture
    return None

def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    cap = cv2.VideoCapture(0)
    cap.set(3, RESOLUTION[0])
    cap.set(4, RESOLUTION[1])

    if not cap.isOpened():
        print("Error: No se puede abrir la cámara")
        return

    celeste_landmarks = mp_drawing.DrawingSpec(color=(255, 206, 135), thickness=2, circle_radius=4)
    celeste_connections = mp_drawing.DrawingSpec(color=(255, 206, 135), thickness=3, circle_radius=2)

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
        model_complexity=1
    ) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_height, image_width, _ = image.shape

            gesture_text = ""
            if results.multi_hand_landmarks:
                for num, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        celeste_landmarks,
                        celeste_connections
                    )
                    lms = extract_landmarks(hand_landmarks, image_width, image_height)
                    hand_positions.append(lms['index_finger_tip'])

                    gesture = recognize_gesture(lms, hand_positions)
                    if gesture:
                        gesture_text = gesture

            if gesture_text:
                cv2.putText(image, gesture_text, (320, 80), cv2.FONT_HERSHEY_SIMPLEX, 2.4, (0, 255, 0), 6)

            cv2.imshow('Lenguaje de Señas - MediaPipe', image)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
            elif key == ord('s'):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_data(image, results, timestamp)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()