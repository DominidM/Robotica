import os

def borrar_archivos_en_directorio(directorio, extensiones):
    """
    Borra todos los archivos con las extensiones indicadas en el directorio y sus subdirectorios.
    NO borra ninguna carpeta, ni siquiera si queda vacía.
    """
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
    if borradas == 0:
        print(f"No se encontraron archivos para borrar en '{directorio}'")
    return borradas

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dataset = os.path.normpath(os.path.join(script_dir, "..", "..", "dataset"))

    # Borra archivos de images
    borrar_archivos_en_directorio(os.path.join(base_dataset, "images"), (".jpg", ".jpeg", ".png"))
    # Borra archivos de landmarks (incluye CSV)
    borrar_archivos_en_directorio(os.path.join(base_dataset, "landmarks"), (".jpg", ".jpeg", ".png", ".csv"))

    # Borra archivos de roboflow splits y todas sus subcarpetas
    roboflow_dir = os.path.join(base_dataset, "roboflow")
    for split in ["train", "test", "valid"]:
        split_dir = os.path.join(roboflow_dir, split)
        borrar_archivos_en_directorio(split_dir, (".jpg", ".jpeg", ".png"))

if __name__ == "__main__":
    main()