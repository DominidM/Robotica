import os

def borrar_archivos_en_directorio(directorio, extensiones):
    borradas = 0
    if not os.path.exists(directorio):
        print(f"Directorio no existe: {directorio}")
        return borradas
    for root, dirs, files in os.walk(directorio):
        for f in files:
            if f.lower().endswith(extensiones):
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

    # Borra imágenes
    borrar_archivos_en_directorio(os.path.join(base_dataset, "images"), (".jpg", ".jpeg", ".png"))
    # Borra landmarks (imágenes y CSV)
    borrar_archivos_en_directorio(os.path.join(base_dataset, "landmarks"), (".jpg", ".jpeg", ".png", ".csv"))

    # Borra de roboflow/train/, roboflow/test/, roboflow/valid/ (imágenes)
    roboflow_dir = os.path.join(base_dataset, "roboflow")
    for split in ["train", "test", "valid"]:
        borrar_archivos_en_directorio(os.path.join(roboflow_dir, split), (".jpg", ".jpeg", ".png"))

if __name__ == "__main__":
    main()