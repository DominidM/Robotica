import cv2
import mediapipe as mp
import time

# --- Pines motores ---
PIN_MOTOR_A_1 = 17
PIN_MOTOR_A_2 = 18
PIN_MOTOR_B_1 = 22
PIN_MOTOR_B_2 = 23

PIN_ENA = 12  # PWM Motor A
PIN_ENB = 13  # PWM Motor B

# --- Pines ultrasonido ---
PIN_TRIG = 5  # HC-SR04 TRIG
PIN_ECHO = 6  # HC-SR04 ECHO

# --- Variables de velocidad ---
VEL_A = 80  # velocidad PWM (0-100)
VEL_B = 80

try:
    import RPi.GPIO as GPIO
    RPI_AVAILABLE = True
except ImportError:
    print("No se encontró la librería RPi.GPIO, corriendo en modo simulación.")
    RPI_AVAILABLE = False

pwmA = None
pwmB = None

def setup():
    global pwmA, pwmB
    if RPI_AVAILABLE:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_MOTOR_A_1, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_A_2, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_B_1, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_B_2, GPIO.OUT)
        GPIO.setup(PIN_ENA, GPIO.OUT)
        GPIO.setup(PIN_ENB, GPIO.OUT)
        GPIO.setup(PIN_TRIG, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        pwmA = GPIO.PWM(PIN_ENA, 1000)
        pwmB = GPIO.PWM(PIN_ENB, 1000)
        pwmA.start(VEL_A)
        pwmB.start(VEL_B)
    print("Motores y ultrasonido listos.")

def set_velocidad(v_a, v_b):
    global pwmA, pwmB
    if RPI_AVAILABLE:
        pwmA.ChangeDutyCycle(v_a)
        pwmB.ChangeDutyCycle(v_b)

def avanzar(tiempo=0.2, v_a=VEL_A, v_b=VEL_B):
    set_velocidad(v_a, v_b)
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

def girar_izquierda(tiempo=0.18, v_a=VEL_A, v_b=VEL_B):
    set_velocidad(v_a, v_b)
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

def girar_derecha(tiempo=0.18, v_a=VEL_A, v_b=VEL_B):
    set_velocidad(v_a, v_b)
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
        set_velocidad(0, 0)

def limpiar():
    if RPI_AVAILABLE:
        pwmA.stop()
        pwmB.stop()
        GPIO.cleanup()
    print("GPIO limpio.")

def distancia_ultrasonido():
    if not RPI_AVAILABLE:
        return 100  # Simula espacio libre
    # Asegura que TRIG esté en bajo
    GPIO.output(PIN_TRIG, False)
    time.sleep(0.01)
    # Pulso de 10us en TRIG
    GPIO.output(PIN_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIG, False)
    pulso_inicio = time.time()
    pulso_fin = time.time()
    timeout = time.time() + 0.05
    # Espera a que ECHO sea HIGH (con timeout de seguridad)
    while GPIO.input(PIN_ECHO) == 0 and time.time() < timeout:
        pulso_inicio = time.time()
    # Espera a que ECHO sea LOW
    while GPIO.input(PIN_ECHO) == 1 and time.time() < timeout:
        pulso_fin = time.time()
    duracion = pulso_fin - pulso_inicio
    distancia = duracion * 17150  # cm
    if distancia < 0 or distancia > 400:  # fuera de rango
        return 400
    return round(distancia, 2)

def prueba_visual_pose():
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    print("Prueba visual: mostrando landmarks del cuerpo. Q para salir.")
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("No se pudo leer el frame de la cámara.")
                break
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image_bgr, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
                )
                # Opcional: muestra algunos puntos clave
                h, w, _ = image_bgr.shape
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.putText(image_bgr, str(id), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,0), 1)
            cv2.imshow('Prueba visual Pose (Q para salir)', image_bgr)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

def seguimiento_por_pose(mostrar=True):
    setup()
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    centro_x_img = ancho // 2

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("No se pudo leer el frame de la cámara.")
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            movimiento = "Detener"

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                lm = results.pose_landmarks.landmark

                # Usar caderas para centro del cuerpo
                left_hip = lm[mp_pose.PoseLandmark.LEFT_HIP]
                right_hip = lm[mp_pose.PoseLandmark.RIGHT_HIP]
                x_centro = int((left_hip.x + right_hip.x) / 2 * ancho)

                if x_centro < centro_x_img - 80:
                    movimiento = "Izquierda"
                    girar_izquierda()
                elif x_centro > centro_x_img + 80:
                    movimiento = "Derecha"
                    girar_derecha()
                else:
                    # Antes de avanzar, revisa el ultrasonido
                    distancia = distancia_ultrasonido()
                    if distancia > 30:
                        movimiento = f"Avanzar ({distancia} cm)"
                        avanzar()
                    else:
                        movimiento = f"Obstáculo a {distancia} cm"
                        detener()
                print(f"Centro cuerpo: {x_centro}, Imagen centro: {centro_x_img}, Movimiento: {movimiento}")

                cv2.putText(image, f"Movimiento: {movimiento}", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
            else:
                print("No se detectó persona.")
                detener()
                cv2.putText(image, f"Movimiento: {movimiento}", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

            if mostrar:
                cv2.imshow('Seguimiento Persona por Pose (Q para salir)', image)
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

    detener()
    cap.release()
    cv2.destroyAllWindows()
    limpiar()

if __name__ == "__main__":
    print("Opciones:\n1. Prueba visual de cuerpo (solo landmarks)\n2. Seguimiento autónomo")
    opcion = input("Selecciona una opción (1/2): ").strip()
    if opcion == "1":
        prueba_visual_pose()
    else:
        seguimiento_por_pose()