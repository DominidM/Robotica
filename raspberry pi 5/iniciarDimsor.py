import os
import uuid
import json
import requests
import pyttsx3
import time
import pygame
import speech_recognition as sr
import random
import string

ROBOT_INFO_FILE = "robot_info.json"
USER_SESSION_FILE = "usuario_sesion.json"

def reproducir_audio():
    try:
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        audio_file = os.path.join(script_dir, 'sonido_inicio.mp3')
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        time.sleep(1)
    except Exception as e:
        print(f"Error reproduciendo audio: {e}")

def reproducir_beep():
    try:
        pygame.mixer.init()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        beep_file = os.path.join(script_dir, 'beep.mp3')
        pygame.mixer.music.load(beep_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except Exception as e:
        print(f"Error reproduciendo beep: {e}")

def hablar(texto):
    try:
        print(f"🔊 Dimsor dice: {texto}")
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.say(texto)
        engine.runAndWait()
        engine.stop()
        del engine
        time.sleep(0.5)
    except Exception as e:
        print(f"❌ Error al hablar: {e}")

def get_mac_address():
    mac = hex(uuid.getnode())[2:].upper()
    return ":".join(mac[i:i+2] for i in range(0, 12, 2))

def guardar_info_local(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f)

def leer_info_local(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def verificar_microfono():
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        input_devices = [
            (i, audio.get_device_info_by_index(i)['name'])
            for i in range(audio.get_device_count())
            if audio.get_device_info_by_index(i)['maxInputChannels'] > 0
        ]
        audio.terminate()
        return bool(input_devices)
    except Exception as e:
        print(f"❌ Error verificando micrófono: {e}")
        return False

def escuchar_nombre():
    try:
        if not verificar_microfono():
            print("❌ No hay micrófono disponible, usando entrada de texto")
            return None
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        print("🎤 Preparando micrófono...")
        with microphone as source:
            print("🎤 Calibrando micrófono para ruido ambiente...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
        hablar("Cuando escuches el beep, di tu nombre.")
        reproducir_beep()
        print("🎤 Escuchando nombre... (20 segundos)")
        with microphone as source:
            audio = recognizer.listen(source, timeout=20, phrase_time_limit=10)
        nombre = recognizer.recognize_google(audio, language='es-ES')
        print(f"✅ Nombre reconocido: {nombre}")
        return nombre.strip()
    except sr.WaitTimeoutError:
        print("⏰ Timeout: No se escuchó nada")
        return None
    except sr.UnknownValueError:
        print("❌ No se pudo entender el audio")
        return None
    except sr.RequestError as e:
        print(f"❌ Error con el servicio de reconocimiento: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado al escuchar: {e}")
        return None

def confirmar_nombre(nombre):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    try:
        hablar("Cuando escuches el beep, confirma si tu nombre es correcto (di sí o no).")
        reproducir_beep()
        with microphone as source:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        respuesta = recognizer.recognize_google(audio, language='es-ES').lower()
        palabras_si = ["sí", "si", "yes", "correcto", "exacto", "afirmativo", "claro"]
        return any(palabra in respuesta for palabra in palabras_si)
    except Exception:
        return False

def generar_registro_key():
    return "-".join(''.join(random.choices(string.ascii_uppercase + string.digits, k=3)) for _ in range(3))

def obtener_ip_local():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def registrar_o_verificar_robot():
    mac = get_mac_address()
    url_get = f"http://localhost:8001/api/robots?identificador_unico={mac}"
    try:
        response = requests.get(url_get)
        if response.status_code == 200 and response.json():
            robot = response.json()[0]
            guardar_info_local({"id": robot["id"], "mac": mac}, ROBOT_INFO_FILE)
            print(f"Robot ya registrado: ID {robot['id']}")
            return robot["id"]
        else:
            payload = {
                "nombre": "RaspberryPi-" + mac[-5:].replace(":", ""),
                "identificador_unico": mac,
                "ip_actual": obtener_ip_local(),
                "estado": "disponible",
                "descripcion": "Robot registrado automáticamente"
            }
            url_post = "http://localhost:8001/api/robots/"
            response = requests.post(url_post, json=payload)
            if response.status_code in (200, 201):
                robot = response.json()
                guardar_info_local({"id": robot["id"], "mac": mac}, ROBOT_INFO_FILE)
                print(f"Robot registrado: ID {robot['id']}")
                return robot["id"]
            elif response.status_code == 409:
                print("Robot ya registrado según la API (409 Conflict)")
                # Obtén el robot existente
                response_get = requests.get(url_get)
                if response_get.status_code == 200 and response_get.json():
                    robot = response_get.json()[0]
                    guardar_info_local({"id": robot["id"], "mac": mac}, ROBOT_INFO_FILE)
                    print(f"Robot registrado: ID {robot['id']}")
                    return robot["id"]
                else:
                    print("No se pudo obtener el robot tras el conflicto 409.")
                    return None
            else:
                print("Error registrando el robot:", response.text)
                return None
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar con el servidor. ¿Está ejecutándose el backend?")
        hablar("Error de conexión con el servidor.")
        return None
    except Exception as e:
        print(f"Error inesperado al registrar el robot: {e}")
        hablar("Ocurrió un error inesperado registrando el robot.")
        return None

# ----- INICIO DEL SCRIPT -----
print("Iniciando DIMSOR...")
reproducir_audio()
hablar("Iniciando DIMSOR")
time.sleep(1)

# ----- Registro/identificación del robot -----
robot_info = leer_info_local(ROBOT_INFO_FILE)
if robot_info:
    robot_id = robot_info["id"]
    print(f"Robot ya identificado. ID: {robot_id}")
else:
    robot_id = registrar_o_verificar_robot()
    print(f"Robot registrado. ID: {robot_id}")

# ----- Registro/identificación del usuario -----
usuario_data = leer_info_local(USER_SESSION_FILE)
if usuario_data:
    nombre = usuario_data["nombre"]
    registro_key = usuario_data["registro_key"]
    rol_id = usuario_data["rol_id"]
    print(f"Bienvenido de nuevo, {nombre} (registro: {registro_key})")
    hablar(f"Bienvenido de nuevo, {nombre}. ¿Listo para comenzar?")
    # Aquí continúa el flujo de diálogo
else:
    print("Hola, soy Dimsor")
    hablar("Hola, soy Dimsor")
    nombre_confirmado = False
    nombre = None
    usa_microfono = verificar_microfono()
    while not nombre_confirmado:
        hablar("¿Cómo te llamas?")
        if usa_microfono:
            nombre = escuchar_nombre()
            if nombre is None or not nombre.strip():
                hablar("No escuché nada, disculpame. Puedes escribir tu nombre:")
                nombre = input("Escribe tu nombre: ").strip()
        else:
            hablar("Por favor, escribe tu nombre")
            nombre = input("Escribe tu nombre: ").strip()
        if not nombre:
            print("No ingresaste ningún nombre. Intentemos de nuevo.")
            continue
        hablar(f"Entendí que tu nombre es {nombre}. ¿Es correcto?")
        confirmado = False
        if usa_microfono:
            confirmado = confirmar_nombre(nombre)
            if not confirmado:
                hablar("Si quieres confirmar, di SÍ o escribe 's' para sí, cualquier otra cosa para no")
                respuesta_texto = input("¿Es correcto? (s/n): ").lower().strip()
                confirmado = respuesta_texto in ['s', 'si', 'sí', 'yes', 'y']
        else:
            respuesta_texto = input("¿Es correcto tu nombre? (s/n): ").lower().strip()
            confirmado = respuesta_texto in ['s', 'si', 'sí', 'yes', 'y']
        if confirmado:
            hablar(f"Perfecto, {nombre}. Procedo a registrarte.")
            nombre_confirmado = True
        else:
            hablar("Entiendo, vamos a intentarlo de nuevo.")

    registro_key = generar_registro_key()
    rol_id = 1  # invitado
    payload = {
        "nombre": nombre,
        "registro_key": registro_key,
        "rol_id": rol_id,
        "robot_id": robot_id
    }
    url_api = "http://localhost:8001/api/usuarios/ingresar"
    try:
        response = requests.post(url_api, json=payload)
        if response.status_code in (200, 201):
            data = response.json()
            registro_key_mostrada = data.get("registro_key", registro_key)
            print(f"Usuario {nombre} registrado correctamente. Tu código de registro es: {registro_key_mostrada}")
            hablar(f"Usuario {nombre} registrado correctamente. Tu código de registro es {registro_key_mostrada}")
            usuario_data = {
                "nombre": nombre,
                "registro_key": registro_key_mostrada,
                "rol_id": rol_id,
                "robot_id": robot_id
            }
            guardar_info_local(usuario_data, USER_SESSION_FILE)
        elif response.status_code == 409:
            try:
                error_data = response.json()
                print("Usuario ya registrado:", error_data)
                hablar("Este usuario ya está registrado. Recuperando información...")
                # Puedes hacer una consulta GET al usuario si tienes endpoint
            except Exception:
                print("Usuario ya registrado pero no se pudo recuperar la información.")
                hablar("Este usuario ya está registrado. Pero no se pudo recuperar la información.")
        else:
            try:
                error_data = response.json()
                print("Error al registrar usuario:", error_data)
                hablar("Hubo un error al registrar el usuario.")
            except Exception:
                print("Error al registrar usuario:", response.text)
                hablar("Hubo un error al registrar el usuario.")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar con el servidor. ¿Está ejecutándose el backend?")
        hablar("Error de conexión con el servidor.")
    except Exception as e:
        print(f"Error inesperado: {e}")
        hablar("Ocurrió un error inesperado.")

print("Programa finalizado.")
hablar("Hasta luego. Que tengas un buen día.")