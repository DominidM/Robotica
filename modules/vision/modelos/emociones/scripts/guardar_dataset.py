import os
import csv

def crear_estructura_dataset(emociones, num_puntos=468):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dataset", "images"))

    for emocion in emociones:
        path = os.path.join(base_dir, emocion)
        os.makedirs(path, exist_ok=True)
        print(f"Carpeta creada o ya existente: {path}")

        csv_path = os.path.join(path, "longitudes_landmarks_emociones.csv")
        if not os.path.exists(csv_path):
            with open(csv_path, "w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=",", quotechar="'", quoting=csv.QUOTE_ALL)
                header = ["nombre_img", "longitud1", "longitud2", "longitud3", "longitud4", "emocion"]
                header += [f"x{i}" for i in range(num_puntos)]
                header += [f"y{i}" for i in range(num_puntos)]
                writer.writerow(header)
            print(f"CSV creado: {csv_path}")

    emociones_csv = os.path.join(base_dir, "..", "emociones.csv")
    with open(emociones_csv, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",", quotechar="'", quoting=csv.QUOTE_ALL)
        writer.writerow(["emocion"])
        for emocion in emociones:
            writer.writerow([emocion])
    print(f"CSV general creado: {emociones_csv}")

if __name__ == "__main__":
    EMOCIONES = ["feliz", "triste", "enojado", "asombrado"]
    crear_estructura_dataset(EMOCIONES)