import csv
import os

def get_csv_roboflow_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "roboflow_all_landmarks.csv"))

def get_output_csv_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "landmarks_global.csv"))

def main():
    csv_roboflow = get_csv_roboflow_path()
    output_csv = get_output_csv_path()
    filas = []
    headers = None

    # Lee el CSV global previo (si existe)
    if os.path.exists(output_csv):
        with open(output_csv, newline='') as f1:
            reader1 = csv.reader(f1)
            headers = next(reader1)
            filas.extend(reader1)

    # Lee el CSV roboflow (roboflow_all_landmarks.csv)
    with open(csv_roboflow, newline='') as f2:
        reader2 = csv.reader(f2)
        h2 = next(reader2)
        headers = h2 if headers is None else headers
        filas.extend(reader2)

    # Opcional: Eliminar duplicados (por alguna columna identificadora, ej: id)
    # filas = [list(x) for x in set(tuple(row) for row in filas)]

    # Escribe el CSV global (sobreescribe, pero con todo combinado)
    with open(output_csv, 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(headers)
        writer.writerows(filas)
    print(f"{len(filas)} filas guardadas en {output_csv}")

if __name__ == "__main__":
    main()