import cv2
import mediapipe as mp
import time

# Motor control (puedes moverlo a otro archivo y hacer import)
try:
    import RPi.GPIO as GPIO
    RPI_AVAILABLE = True
except ImportError:
    print("No se encontró la librería RPi.GPIO, corriendo en modo simulación.")
    RPI_AVAILABLE = False

PIN_MOTOR_A_1 = 17
PIN_MOTOR_A_2 = 18
PIN_MOTOR_B_1 = 22
PIN_MOTOR_B_2 = 23

def setup():
    if RPI_AVAILABLE:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_MOTOR_A_1, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_A_2, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_B_1, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_B_2, GPIO.OUT)
    print("Motores listos.")

def avanzar(tiempo=0.2):
    print("Avanzando..." if RPI_AVAILABLE else "Avanzando... (simulación)")
    if RPI_AVAILABLE:
        GPIO.output(PIN_MOTOR_A_1, GPIO.HIGH)
        GPIO.output(PIN_MOTOR_A_2, GPIO.LOW)
        GPIO.output(PIN_MOTOR_B_1, GPIO.HIGH)
        GPIO.output(PIN_MOTOR_B_2, GPIO.LOW)
        time.sleep(tiempo)
        detener()
    else:
        time.sleep(tiempo)

def girar_izquierda(tiempo=0.15):
    print("Girando a la izquierda..." if RPI_AVAILABLE else "Girando a la izquierda... (simulación)")
    if RPI_AVAILABLE:
        GPIO.output(PIN_MOTOR_A_1, GPIO.LOW)
        GPIO.output(PIN_MOTOR_A_2, GPIO.HIGH)
        GPIO.output(PIN_MOTOR_B_1, GPIO.HIGH)
        GPIO.output(PIN_MOTOR_B_2, GPIO.LOW)
        time.sleep(tiempo)
        detener()
    else:
        time.sleep(tiempo)

def girar_derecha(tiempo=0.15):
    print("Girando a la derecha..." if RPI_AVAILABLE else "Girando a la derecha... (simulación)")
    if RPI_AVAILABLE:
        GPIO.output(PIN_MOTOR_A_1, GPIO.HIGH)
        GPIO.output(PIN_MOTOR_A_2, GPIO.LOW)
        GPIO.output(PIN_MOTOR_B_1, GPIO.LOW)
        GPIO.output(PIN_MOTOR_B_2, GPIO.HIGH)
        time.sleep(tiempo)
        detener()
    else:
        time.sleep(tiempo)

def detener():
    print("Deteniendo motores." if RPI_AVAILABLE else "Deteniendo motores. (simulación)")
    if RPI_AVAILABLE:
        GPIO.output(PIN_MOTOR_A_1, GPIO.LOW)
        GPIO.output(PIN_MOTOR_A_2, GPIO.LOW)
        GPIO.output(PIN_MOTOR_B_1, GPIO.LOW)
        GPIO.output(PIN_MOTOR_B_2, GPIO.LOW)

def limpiar():
    if RPI_AVAILABLE:
        GPIO.cleanup()
    print("GPIO limpio.")

# --- Seguimiento por cámara ---
def seguimiento_por_camara(mostrar=True):
    setup()
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    centro_x_img = ancho // 2

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("No se pudo leer el frame de la cámara.")
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            movimiento = None

            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(image, detection)
                    bbox = detection.location_data.relative_bounding_box
                    x_face = int(bbox.xmin * ancho + bbox.width * ancho / 2)

                    # Lógica de movimiento
                    if x_face < centro_x_img - 80:
                        movimiento = "izquierda"
                        girar_izquierda()
                    elif x_face > centro_x_img + 80:
                        movimiento = "derecha"
                        girar_derecha()
                    else:
                        movimiento = "avanzar"
                        avanzar()
                    
                    print(f"Cara detectada! Movimiento: {movimiento}")

                    break  # Solo sigue la primera cara detectada

            else:
                print("No se detectó ninguna cara.")
                detener()

            if mostrar:
                cv2.imshow('Seguimiento Persona (Presiona Q para salir)', image)
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

    detener()
    cap.release()
    cv2.destroyAllWindows()
    limpiar()

if __name__ == "__main__":
    seguimiento_por_camara()