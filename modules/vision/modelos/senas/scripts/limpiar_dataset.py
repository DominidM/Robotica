import os
import glob

# Carpetas con imágenes originales
image_dirs = [
    "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/roboflow/train/",
    "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/roboflow/valid/",
    "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/roboflow/test/",
]

# Carpetas con landmarks CSV individuales
landmark_dirs = [
    "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/landmarks/train/",
    "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/landmarks/valid/",
    "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/landmarks/test/",
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