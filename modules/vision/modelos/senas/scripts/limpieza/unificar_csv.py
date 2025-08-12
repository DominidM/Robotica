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

    # Lee el CSV roboflow (roboflow_all_landmarks.csv)
    with open(csv_roboflow, newline='') as f2:
        reader2 = csv.reader(f2)
        h2 = next(reader2)
        headers = h2
        for row in reader2:
            filas.append(row)

    # Escribe el CSV global
    with open(output_csv, 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(headers)
        writer.writerows(filas)
    print(f"{len(filas)} filas guardadas en {output_csv}")

if __name__ == "__main__":
    main()