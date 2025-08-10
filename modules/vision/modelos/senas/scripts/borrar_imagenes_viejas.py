import os
import glob

# Carpeta base del script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Carpetas con imágenes originales (rutas relativas)
image_dirs = [
    os.path.join(script_dir, "..", "dataset", "roboflow", "train"),
    os.path.join(script_dir, "..", "dataset", "roboflow", "valid"),
    os.path.join(script_dir, "..", "dataset", "roboflow", "test"),
]

# Carpetas con landmarks CSV individuales (rutas relativas)
landmark_dirs = [
    os.path.join(script_dir, "..", "dataset", "landmarks", "train"),
    os.path.join(script_dir, "..", "dataset", "landmarks", "valid"),
    os.path.join(script_dir, "..", "dataset", "landmarks", "test"),
]

def borrar_archivos(directorio, patrones):
    for patron in patrones:
        archivos = glob.glob(os.path.join(directorio, patron))
        for archivo in archivos:
            try:
                os.remove(archivo)
                print(f"Borrado: {archivo}")
            except Exception as e:
                print(f"Error al borrar {archivo}: {e}")

# Eliminar imágenes originales
for img_dir in image_dirs:
    borrar_archivos(img_dir, ['*.jpg', '*.png'])

# Eliminar CSV de landmarks individuales
for lm_dir in landmark_dirs:
    borrar_archivos(lm_dir, ['*.csv'])

print("\n¡Limpieza completada! Solo queda all_landmarks.csv y tus scripts.")