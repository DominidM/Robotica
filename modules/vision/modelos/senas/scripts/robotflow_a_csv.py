import cv2
import mediapipe as mp
import os
import csv

mp_hands = mp.solutions.hands

splits = ["train", "valid", "test"]
base_input_dir = "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/roboflow/"
base_output_dir = "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/landmarks/"
resize_dim = (320, 320)  # Puedes ajustar el tamaño aquí

def preprocess_image(image):
    # Si la imagen es en escala de grises, conviértela a color
    if len(image.shape) == 2 or image.shape[2] == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # Redimensiona la imagen para estandarizar entrada
    image = cv2.resize(image, resize_dim)
    # Mejora el contraste usando histogram equalization
    img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    image = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return image

for split in splits:
    input_dir = os.path.join(base_input_dir, split)
    output_dir = os.path.join(base_output_dir, split)
    os.makedirs(output_dir, exist_ok=True)

    print(f"Procesando {split}: {input_dir}")
    not_detected_log = os.path.join(output_dir, "not_detected.txt")
    total_imgs, detected = 0, 0

    with open(not_detected_log, "w") as logf, mp_hands.Hands(static_image_mode=True, max_num_hands=1) as hands:
        for img_name in os.listdir(input_dir):
            if img_name.lower().endswith(('.jpg', '.png')):
                image_path = os.path.join(input_dir, img_name)
                image = cv2.imread(image_path)
                total_imgs += 1
                if image is None:
                    print(f"Error leyendo imagen {image_path}")
                    logf.write(f"Error leyendo: {image_path}\n")
                    continue
                # Preprocesamiento
                image = preprocess_image(image)
                results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                if results.multi_hand_landmarks:
                    detected += 1
                    for hand_landmarks in results.multi_hand_landmarks:
                        csv_name = img_name.rsplit('.', 1)[0] + '.csv'
                        csv_path = os.path.join(output_dir, csv_name)
                        with open(csv_path, mode='w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(["landmark_index", "x", "y", "z"])
                            for idx, lm in enumerate(hand_landmarks.landmark):
                                writer.writerow([idx, lm.x, lm.y, lm.z])
                else:
                    print(f"No se detectaron manos en {image_path}")
                    logf.write(f"No se detectaron manos: {image_path}\n")
    print(f"Landmarks de {split} guardados en {output_dir}")
    print(f"Imágenes procesadas: {total_imgs}, con landmarks detectados: {detected}, sin landmarks: {total_imgs-detected}\n")