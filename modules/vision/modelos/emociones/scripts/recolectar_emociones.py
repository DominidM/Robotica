import cv2
import mediapipe as mp
import math
import csv
import os
import time

def recolectar_emocion(emocion, cam_index=0):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dataset", "images", emocion))
    os.makedirs(base_dir, exist_ok=True)
    csv_path = os.path.join(base_dir, "longitudes_landmarks_emociones.csv")

    cap = cv2.VideoCapture(cam_index)
    cap.set(3, 1280)
    cap.set(4, 720)

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True,
                                      min_detection_confidence=0.5, min_tracking_confidence=0.5)

    print(f"Presiona ESPACIO para guardar imagen y datos con emoción '{emocion}'. ESC para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        landmarks_x, landmarks_y = [], []
        rostro_detectado = False

        if results.multi_face_landmarks:
            for rostro in results.multi_face_landmarks:
                alto, ancho, _ = frame.shape
                lista = []
                for puntos in rostro.landmark:
                    x = int(puntos.x * ancho)
                    y = int(puntos.y * alto)
                    landmarks_x.append(x)
                    landmarks_y.append(y)
                    lista.append((x, y))

                if len(lista) == 468:
                    rostro_detectado = True
                    # Longitudes de referencia:
                    x1, y1 = lista[65]
                    x2, y2 = lista[158]
                    longitud1 = math.hypot(x2 - x1, y2 - y1)
                    x3, y3 = lista[295]
                    x4, y4 = lista[385]
                    longitud2 = math.hypot(x4 - x3, y4 - y3)
                    x5, y5 = lista[78]
                    x6, y6 = lista[308]
                    longitud3 = math.hypot(x6 - x5, y6 - y5)
                    x7, y7 = lista[13]
                    x8, y8 = lista[14]
                    longitud4 = math.hypot(x8 - x7, y8 - y7)

        cv2.putText(frame, f'Emocion: {emocion}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
        if rostro_detectado:
            cv2.putText(frame, 'Rostro detectado', (10,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        else:
            cv2.putText(frame, 'No hay rostro', (10,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.imshow(f'Recolección de emociones: {emocion}', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            break
        elif key == 32 and rostro_detectado:  # ESPACIO
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            img_name = f"{emocion}_{timestamp}.jpg"
            img_path = os.path.join(base_dir, img_name)
            cv2.imwrite(img_path, frame)
            # Guarda datos en CSV
            with open(csv_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([img_name, longitud1, longitud2, longitud3, longitud4, emocion] + landmarks_x + landmarks_y)
            print(f"Guardado: {img_name} / longitudes en CSV")
            time.sleep(0.5)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    emocion = sys.argv[1] if len(sys.argv) > 1 else "feliz"
    recolectar_emocion(emocion)