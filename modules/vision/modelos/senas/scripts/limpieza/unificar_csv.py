import csv
import os

def get_csv_local_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "all_landmarks.csv"))

def get_csv_roboflow_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "roboflow_all_landmarks.csv"))

def get_output_csv_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "landmarks_global.csv"))

def main():
    csv_local = get_csv_local_path()
    csv_roboflow = get_csv_roboflow_path()
    output_csv = get_output_csv_path()
    filas = []
    headers = None

    # Lee el CSV local (all_landmarks.csv)
    with open(csv_local, newline='') as f1:
        reader1 = csv.reader(f1)
        h1 = next(reader1)
        # Si no tiene partition, la agrega vacía
        if "partition" not in h1:
            h1 = ["partition"] + h1
            partition_index = 0
            clase_index = 1
            data_start = 2
        else:
            partition_index = h1.index("partition")
            clase_index = h1.index("clase")
            data_start = h1.index("clase") + 1
        if headers is None:
            headers = h1
        for row in reader1:
            if len(row) == len(h1)-1:
                row = [""] + row  # Partition vacío
            filas.append(row)

    # Lee el CSV roboflow (roboflow_all_landmarks.csv)
    with open(csv_roboflow, newline='') as f2:
        reader2 = csv.reader(f2)
        h2 = next(reader2)
        if headers is None:
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