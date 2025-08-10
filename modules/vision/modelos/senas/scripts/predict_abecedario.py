import os
import cv2
import mediapipe as mp
import numpy as np
import joblib

# Obtén la ruta absoluta del modelo usando la ubicación del script
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "..", "models", "abecedario_model.pkl")
model = joblib.load(model_path)

mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    model_complexity=1
) as hands:
    recognized_text = ""
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y, lm.z])
                
                # Predice la letra
                letter_pred = model.predict([landmarks])[0]
                
                cv2.putText(image, f'Letra: {letter_pred}', (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (0,255,0), 6)
                recognized_text += letter_pred
        
        cv2.putText(image, f'Texto: {recognized_text}', (60, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3)
        cv2.imshow('Abecedario en Señas', image)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == ord('c'):
            recognized_text = ""  # Limpiar texto
cap.release()
cv2.destroyAllWindows()