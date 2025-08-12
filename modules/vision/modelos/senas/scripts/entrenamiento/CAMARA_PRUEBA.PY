import cv2
import joblib
import numpy as np
import os

# Si tienes MediaPipe:
try:
    import mediapipe as mp
    USE_MEDIAPIPE = True
except ImportError:
    USE_MEDIAPIPE = False

def obtener_landmarks(frame):
    # Si tienes MediaPipe instalado, usarlo para obtener landmarks
    if USE_MEDIAPIPE:
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        hands.close()
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            # Extrae x, y, z para los 21 puntos
            lm = []
            for landmark in hand_landmarks.landmark:
                lm.extend([landmark.x, landmark.y, landmark.z])
            return np.array(lm).reshape(1, -1)
        else:
            return None
    else:
        # Simulación si no tienes MediaPipe, ¡no sirve para predicción real!
        return np.random.rand(1, 63)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.normpath(os.path.join(script_dir, "..", "..", "models", "abecedario_model.pkl"))
    model = joblib.load(model_path)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return

    print("Presiona 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el frame.")
            break

        landmarks = obtener_landmarks(frame)

        if landmarks is not None and landmarks.shape[1] == 63:
            pred = model.predict(landmarks)[0]
            cv2.putText(frame, f'Prediccion: {pred}', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        else:
            cv2.putText(frame, 'Sin mano detectada', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.imshow('Camara Prueba', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()