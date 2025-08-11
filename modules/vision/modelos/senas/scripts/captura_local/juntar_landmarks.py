import os
import csv

def get_landmarks_base_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "landmarks"))

def get_output_csv_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "all_landmarks.csv"))

def main():
    landmarks_base = get_landmarks_base_dir()
    output_csv = get_output_csv_path()
    clases = [d for d in os.listdir(landmarks_base) if os.path.isdir(os.path.join(landmarks_base, d))]
    filas = []
    for clase in clases:
        clase_lm_dir = os.path.join(landmarks_base, clase)
        for archivo in os.listdir(clase_lm_dir):
            if archivo.lower().endswith(".csv"):
                csv_path = os.path.join(clase_lm_dir, archivo)
                with open(csv_path, 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        # Agrega la clase como primer elemento
                        filas.append([clase] + row)
    # Escribe todas las filas al archivo global
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["clase"] + [f"x{i+1}" for i in range(len(filas[0])-1)])  # encabezado
        writer.writerows(filas)
    print(f"{len(filas)} filas guardadas en {output_csv}")

if __name__ == "__main__":
    main()