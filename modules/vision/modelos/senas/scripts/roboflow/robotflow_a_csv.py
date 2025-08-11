import os
import csv

def get_landmarks_base_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "landmarks"))

def get_output_csv_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "roboflow_all_landmarks.csv"))

def main():
    landmarks_base = get_landmarks_base_dir()
    output_csv = get_output_csv_path()
    filas = []
    for clase in os.listdir(landmarks_base):
        clase_lm_dir = os.path.join(landmarks_base, clase)
        if not os.path.isdir(clase_lm_dir): continue
        for archivo in os.listdir(clase_lm_dir):
            if archivo.startswith("roboflow_") and archivo.endswith(".csv"):
                # Ejemplo nombre: roboflow_train_img123.csv
                parts = archivo.split('_')
                if len(parts) < 3: continue
                partition = parts[1]
                csv_path = os.path.join(clase_lm_dir, archivo)
                with open(csv_path, 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        filas.append([partition, clase] + row)
    # Escribe el archivo global
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        if filas:
            writer.writerow(["partition", "clase"] + [f"x{i+1}" for i in range(len(filas[0])-2)])
            writer.writerows(filas)
    print(f"{len(filas)} filas guardadas en {output_csv}")

if __name__ == "__main__":
    main()