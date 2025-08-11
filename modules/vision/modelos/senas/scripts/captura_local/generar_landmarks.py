import os
import cv2
import mediapipe as mp
import csv

def get_images_base_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "images"))

def get_landmarks_base_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "landmarks"))

def procesar_imagen(imagen_path):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
    image = cv2.imread(imagen_path)
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        # Devuelve lista de [x1, y1, z1, x2, y2, z2, ..., x21, y21, z21]
        return [coord for lm in results.multi_hand_landmarks[0].landmark 
                for coord in (lm.x, lm.y, lm.z)]
    else:
        return None  # No se detectó mano

def guardar_landmarks_csv(landmarks, csv_path):
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(landmarks)

def main():
    images_base = get_images_base_dir()
    landmarks_base = get_landmarks_base_dir()
    clases = [d for d in os.listdir(images_base) if os.path.isdir(os.path.join(images_base, d))]
    for clase in clases:
        clase_img_dir = os.path.join(images_base, clase)
        clase_lm_dir = os.path.join(landmarks_base, clase)
        os.makedirs(clase_lm_dir, exist_ok=True)
        for archivo in os.listdir(clase_img_dir):
            if archivo.lower().endswith(".jpg"):
                img_path = os.path.join(clase_img_dir, archivo)
                csv_name = os.path.splitext(archivo)[0] + ".csv"
                csv_path = os.path.join(clase_lm_dir, csv_name)
                if os.path.exists(csv_path):
                    print(f"Ya existe: {csv_path}, omitiendo...")
                    continue
                landmarks = procesar_imagen(img_path)
                if landmarks:
                    guardar_landmarks_csv(landmarks, csv_path)
                    print(f"Landmarks guardados: {csv_path}")
                else:
                    print(f"No se detectó mano en {img_path}, no se guardó landmarks.")

if __name__ == "__main__":
    main()