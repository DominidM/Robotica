import cv2
import os
import time

CLASES_VALIDAS = [str(i) for i in range(10)]
CLASES_VALIDAS += list("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")
CLASES_VALIDAS += ["BIEN", "ESPACIO", "MAL", "PARE"]

def get_base_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Ruta relativa, portable para cualquier PC y colaborador
    base_dir = os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "images"))
    return base_dir

def pedir_clase():
    print("Clases válidas: " + ", ".join(CLASES_VALIDAS))
    print("¿Qué letra, número o gesto estás mostrando? (Ejemplo: A, B, 0, 1, BIEN, ESPACIO, MAL, PARE)")
    clase = input("Clase: ").strip().upper()
    if clase not in CLASES_VALIDAS:
        print("Clase invalida. Intenta de nuevo.")
        return None
    return clase

def capturar_y_guardar(clase, cam_id=0):
    base_dir = get_base_dir()
    clase_dir = os.path.join(base_dir, clase)
    os.makedirs(clase_dir, exist_ok=True)

    cap = cv2.VideoCapture(cam_id)
    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return

    print(f"Presiona ESPACIO para capturar imagen ({clase}), ESC para salir.")
    contador = len([f for f in os.listdir(clase_dir) if f.endswith(".jpg")])

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar imagen.")
            break

        cv2.imshow(f"Captura - Clase: {clase}", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC para salir
            break
        elif key == 32:  # ESPACIO para guardar imagen
            nombre_img = f"{clase}{contador:03d}.jpg"
            ruta_img = os.path.join(clase_dir, nombre_img)
            cv2.imwrite(ruta_img, frame)
            print(f"Imagen guardada: {ruta_img}")
            contador += 1
            time.sleep(0.5)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    while True:
        clase = pedir_clase()
        if not clase:
            print("Clase vacía o inválida. Saliendo.")
            break
        capturar_y_guardar(clase)
        salir = input("¿Quieres capturar otra clase? (s/n): ").strip().lower()
        if salir != 's':
            break

