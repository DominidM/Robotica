import os
import csv
import glob
import pandas as pd

csv_path = "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/all_landmarks.csv"
landmark_dirs = [
    "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/landmarks/train/",
    "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/landmarks/valid/",
    "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/landmarks/test/",
]

# 1. Cargar nombres de imágenes existentes en el CSV
df = pd.read_csv(csv_path)
imagenes_existentes = set(df['image'].values)

# 2. Abrir el CSV en modo append y agregar solo los nuevos landmarks
with open(csv_path, "a", newline='') as out_f:
    writer = csv.writer(out_f)
    for landmark_dir in landmark_dirs:
        for landmark_file in glob.glob(os.path.join(landmark_dir, "*.csv")):
            base = os.path.basename(landmark_file)
            if base in imagenes_existentes:
                continue  # Ya está en el CSV
            label = base.split("_")[0][0]  # Ajusta si tus etiquetas vienen distinto
            with open(landmark_file, "r") as f:
                reader = csv.DictReader(f)
                coords = []
                for row in reader:
                    coords.extend([row["x"], row["y"], row["z"]])
                if len(coords) != 63:
                    continue
                writer.writerow(coords + [label, base])

print("Se agregaron solo los landmarks nuevos, sin duplicados.")