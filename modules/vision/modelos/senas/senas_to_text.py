import os
import joblib
import pandas as pd
import cv2

# Rutas y carga modelo
script_dir = os.path.dirname(os.path.abspath(__file__))
modelo_path = os.path.normpath(os.path.join(script_dir, "models", "abecedario_model.pkl"))

try:
    modelo = joblib.load(modelo_path)
except Exception as e:
    print("No se pudo cargar el modelo:", e)
    exit()

def hablar(texto):
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.say(texto)
    engine.runAndWait()
    engine.stop()
    del engine

def mostrar_camara():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return
    print("Presiona 'q' para salir de la cámara.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo obtener frame de la cámara.")
            break
        cv2.imshow('Vista Cámara Señal', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Cerrando cámara.")
            break
    cap.release()
    cv2.destroyAllWindows()

def detectar_letra_por_camara():
    # Muestra la cámara para referencia visual (desarrollo)
    mostrar_camara()
    # Simula pipeline: pedir CSV de landmarks por consola
    csv_path = input("Ruta CSV de landmarks de la imagen/seña (o ENTER para terminar): ").strip()
    if not csv_path:
        return None
    if not os.path.exists(csv_path):
        print("Archivo no encontrado.")
        return None
    df = pd.read_csv(csv_path, header=None)
    X = df.values.reshape(1, -1)
    letra = modelo.predict(X)[0]
    return letra

def senas_a_texto():
    print("Transforma señas a texto. Se muestra tu cámara para referencia.")
    print("Ingresa CSV de cada seña, ENTER para finalizar.")
    print("Si tu modelo predice 'ESPACIO', se agrega un espacio. Si predice 'FIN', termina la frase.")
    texto = ""
    while True:
        letra = detectar_letra_por_camara()
        if letra is None:
            break
        letra_str = str(letra).upper()
        # Si detecta "FIN", termina
        if letra_str == "FIN":
            print("Seña 'FIN' detectada. Deteniendo transcripción.")
            hablar("Frase finalizada")
            break
        elif letra_str == "ESPACIO":
            texto += " "
            print("Texto actual:", texto)
            hablar("espacio")
        elif letra_str.isalpha() and len(letra_str) == 1:
            texto += letra_str
            print("Texto actual:", texto)
            hablar(letra_str)
        else:
            print(f"Seña '{letra_str}' no reconocida como letra o comando.")
    print(f"\nTexto final obtenido: {texto}")
    hablar(f"Texto final obtenido: {texto}")

if __name__ == "__main__":
    senas_a_texto()