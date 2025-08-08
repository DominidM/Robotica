import time

try:
    import RPi.GPIO as GPIO
    RPI_AVAILABLE = True
except ImportError:
    print("No se encontró la librería RPi.GPIO, corriendo en modo simulación.")
    RPI_AVAILABLE = False

# Pines de control de los motores (ajusta según tu conexión)
PIN_MOTOR_A_1 = 17  # IN1
PIN_MOTOR_A_2 = 18  # IN2
PIN_MOTOR_B_1 = 22  # IN3
PIN_MOTOR_B_2 = 23  # IN4

def setup():
    if RPI_AVAILABLE:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_MOTOR_A_1, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_A_2, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_B_1, GPIO.OUT)
        GPIO.setup(PIN_MOTOR_B_2, GPIO.OUT)
    print("Motores listos.")

def avanzar(tiempo=1):
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

def retroceder(tiempo=1):
    print("Retrocediendo..." if RPI_AVAILABLE else "Retrocediendo... (simulación)")
    if RPI_AVAILABLE:
        GPIO.output(PIN_MOTOR_A_1, GPIO.LOW)
        GPIO.output(PIN_MOTOR_A_2, GPIO.HIGH)
        GPIO.output(PIN_MOTOR_B_1, GPIO.LOW)
        GPIO.output(PIN_MOTOR_B_2, GPIO.HIGH)
        time.sleep(tiempo)
        detener()
    else:
        time.sleep(tiempo)

def girar_izquierda(tiempo=0.5):
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

def girar_derecha(tiempo=0.5):
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

if __name__ == "__main__":
    setup()
    avanzar(2)
    girar_izquierda(1)
    retroceder(1)
    detener()
    limpiar()