import os

def borrar_imagenes_en_directorio(directorio):
    borradas = 0
    if not os.path.exists(directorio):
        return borradas
    for root, dirs, files in os.walk(directorio):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(root, f)
                try:
                    os.remove(path)
                    borradas += 1
                    print(f"Borrada: {path}")
                except Exception as e:
                    print(f"No se pudo borrar {path}: {e}")
    return borradas

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dataset = os.path.normpath(os.path.join(script_dir, "..", "..", "dataset"))

    # Borra de images/
    total_images = borrar_imagenes_en_directorio(os.path.join(base_dataset, "images"))
    # Borra de landmarks/ (solo imágenes, no .csv)
    total_landmarks = borrar_imagenes_en_directorio(os.path.join(base_dataset, "landmarks"))

    # Borra de roboflow/train/, roboflow/test/, roboflow/valid/
    roboflow_dir = os.path.join(base_dataset, "roboflow")
    for split in ["train", "test", "valid"]:
        total_rf = borrar_imagenes_en_directorio(os.path.join(roboflow_dir, split))
        print(f"Borradas en roboflow/{split}: {total_rf}")

    print(f"Borradas en images/: {total_images}")
    print(f"Borradas en landmarks/: {total_landmarks}")

if __name__ == "__main__":
    main()