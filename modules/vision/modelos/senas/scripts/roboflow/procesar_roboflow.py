import os
import cv2
import mediapipe as mp
import csv

def get_roboflow_base_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "roboflow"))

def get_landmarks_base_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "landmarks"))

def procesar_imagen(imagen_path):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
    image = cv2.imread(imagen_path)
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        return [coord for lm in results.multi_hand_landmarks[0].landmark for coord in (lm.x, lm.y, lm.z)]
    else:
        return None

def guardar_landmarks_csv(landmarks, csv_path):
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(landmarks)

def main():
    roboflow_base = get_roboflow_base_dir()
    landmarks_base = get_landmarks_base_dir()
    partitions = ["train", "test", "valid"]
    for partition in partitions:
        partition_dir = os.path.join(roboflow_base, partition)
        if not os.path.exists(partition_dir): continue
        clases = [d for d in os.listdir(partition_dir) if os.path.isdir(os.path.join(partition_dir, d))]
        for clase in clases:
            clase_rf_dir = os.path.join(partition_dir, clase)
            clase_lm_dir = os.path.join(landmarks_base, clase)
            os.makedirs(clase_lm_dir, exist_ok=True)
            for img_file in os.listdir(clase_rf_dir):
                if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                    img_path = os.path.join(clase_rf_dir, img_file)
                    csv_name = f"roboflow_{partition}_{os.path.splitext(img_file)[0]}.csv"
                    csv_path = os.path.join(clase_lm_dir, csv_name)
                    if os.path.exists(csv_path): continue
                    landmarks = procesar_imagen(img_path)
                    if landmarks:
                        guardar_landmarks_csv(landmarks, csv_path)
                        print(f"Landmarks guardados: {csv_path}")
                    else:
                        print(f"No mano detectada en: {img_path}")

if __name__ == "__main__":
    main()