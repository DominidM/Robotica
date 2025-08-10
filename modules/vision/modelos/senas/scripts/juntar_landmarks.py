import os
import csv
import glob

# Carpeta donde están los landmarks
landmark_dirs = [
    "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/landmarks/train/",
    "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/landmarks/valid/",
    "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/landmarks/test/",
]

# Archivo de salida unificado
output_csv = "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/all_landmarks.csv"

with open(output_csv, "w", newline='') as out_f:
    writer = csv.writer(out_f)
    # Escribe cabecera: landmark_0_x, landmark_0_y, landmark_0_z, ..., landmark_20_z, label, imagen
    header = []
    for i in range(21):  # 21 landmarks
        header.extend([f"lm_{i}_x", f"lm_{i}_y", f"lm_{i}_z"])
    header += ["label", "image"]
    writer.writerow(header)

    for landmark_dir in landmark_dirs:
        for landmark_file in glob.glob(os.path.join(landmark_dir, "*.csv")):
            # Extraer etiqueta (ajusta esto según tu dataset)
            # Ejemplo: si el nombre es "A_12345.csv", la etiqueta es "A"
            base = os.path.basename(landmark_file)
            # Puedes ajustar esta línea según tu formato de nombre/etiqueta
            label = base.split("_")[0][0]  # Ejemplo: "A" de "A_xxxx.csv"
            # Si tienes una forma más precisa de obtener la etiqueta, cámbiala aquí

            with open(landmark_file, "r") as f:
                reader = csv.DictReader(f)
                coords = []
                for row in reader:
                    coords.extend([row["x"], row["y"], row["z"]])
                # Si no tiene 21 landmarks, ignora
                if len(coords) != 63:
                    continue
                # Escribe fila: coords + label + imagen
                writer.writerow(coords + [label, base])

print(f"Landmarks unificados en: {output_csv}")