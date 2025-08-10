import os
import csv
import glob

# Ubicación del script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Carpetas donde están los landmarks (rutas relativas)
landmark_dirs = [
    os.path.join(script_dir, "..", "dataset", "landmarks", "train"),
    os.path.join(script_dir, "..", "dataset", "landmarks", "valid"),
    os.path.join(script_dir, "..", "dataset", "landmarks", "test"),
]

# Archivo de salida unificado (ruta relativa)
output_csv = os.path.join(script_dir, "..", "dataset", "all_landmarks.csv")

with open(output_csv, "w", newline='') as out_f:
    writer = csv.writer(out_f)
    # Escribe cabecera: lm_0_x, lm_0_y, ..., lm_20_z, label, image
    header = []
    for i in range(21):  # 21 landmarks
        header.extend([f"lm_{i}_x", f"lm_{i}_y", f"lm_{i}_z"])
    header += ["label", "image"]
    writer.writerow(header)

    for landmark_dir in landmark_dirs:
        for landmark_file in glob.glob(os.path.join(landmark_dir, "*.csv")):
            base = os.path.basename(landmark_file)
            label = base.split("_")[0][0]  # Ajusta si tu formato cambia
            with open(landmark_file, "r") as f:
                reader = csv.DictReader(f)
                coords = []
                for row in reader:
                    coords.extend([row["x"], row["y"], row["z"]])
                if len(coords) != 63:
                    continue  # Solo archivos con 21 landmarks
                writer.writerow(coords + [label, base])

print(f"Landmarks unificados en: {output_csv}")