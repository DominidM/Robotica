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
from datetime import datetime

# --- Importa los chatbots y motores ---
from modules.chatbot.core import predict_class, get_response, retrieval_response
from modules.test_psico.test_zung import (
    cargar_preguntas, respuesta_a_valor, interpretar_zung,
    guardar_resultado, cargar_usuario, ultimo_resultado_usuario,
)
from modules.chatbot.inferencia import iniciar_chatbot_texto
from modules.chatbot.voz import iniciar_chatbot_voz, listen, speak
from modules.vision.seguimiento_persona import seguimiento_por_camara

# --- Importa PIL y tkinter para los ojos animados ---
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
import threading

# --- Configuración de archivo ---
ROBOT_INFO_FILE = "config/robot_info.json"
USER_SESSION_FILE = "config/usuario_sesion.json"
SESION_ACTUAL_FILE = "config/sesion_actual.json"

# --- Parámetros para animación de ojos ---
WIDTH, HEIGHT = 479, 202
BG_COLOR = (20, 30, 35)
EYE_COLOR = (150, 255, 255)
TEXT_COLOR = (106, 191, 210)

def draw_robot_face(left_eye_x, right_eye_x, eye_y, eye_radius):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw.ellipse([0, 0, WIDTH, HEIGHT*2], fill=BG_COLOR)
    draw.pieslice([left_eye_x-eye_radius, eye_y-eye_radius, left_eye_x+eye_radius, eye_y+eye_radius+45], 180, 360, fill=EYE_COLOR)
    draw.pieslice([right_eye_x-eye_radius, eye_y-eye_radius, right_eye_x+eye_radius, eye_y+eye_radius+45], 180, 360, fill=EYE_COLOR)
    try:
        font = ImageFont.truetype("arialbd.ttf", 23)
    except:
        font = ImageFont.load_default()
    draw.text((40, HEIGHT-35), "SG DIMSOR", font=font, fill=TEXT_COLOR)
    return img

class RobotEyesApp:
    def __init__(self, master):
        self.master = master
        master.title("Simulación Ojos Robot - SG DIMSOR")
        self.label = tk.Label(master)
        self.label.pack()
        self.frame = 0
        self.animate()

    def animate(self):
        if self.frame < 20:
            left_eye_x = 145 + self.frame*2
            right_eye_x = 285 + self.frame*2
        else:
            left_eye_x = 145 + (39-self.frame)*2
            right_eye_x = 285 + (39-self.frame)*2
        img = draw_robot_face(left_eye_x, right_eye_x, 110, 45)
        tk_img = ImageTk.PhotoImage(img)
        self.label.imgtk = tk_img
        self.label.configure(image=tk_img)
        self.frame = (self.frame + 1) % 40
        self.master.after(80, self.animate)

def mostrar_ojos_robot():
    root = tk.Tk()
    app = RobotEyesApp(root)
    root.mainloop()

def reproducir_audio():
    try:
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        audio_file = os.path.join(script_dir, 'sound/sonido_inicio.mp3')
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
        beep_file = os.path.join(script_dir, 'sound/beep.mp3')
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

def verificar_microfono_voz():
    try:
        mic_list = sr.Microphone.list_microphone_names()
        return bool(mic_list)
    except Exception:
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

def comando_seguimiento(msg):
    return any(palabra in msg.lower() for palabra in ["sígueme", "seguime", "sígame", "seguir", "sigueme"])

def seguir_persona():
    hablar("Iniciando modo seguimiento por cámara. Di 'detente' o presiona Q para parar.")
    try:
        seguimiento_por_camara(mostrar=True)
        hablar("Modo seguimiento detenido.")
    except Exception as e:
        print(f"Error en el modo seguimiento: {e}")
        hablar("Ocurrió un error en el modo seguimiento.")

def crear_sesion_api(usuario_id, robot_id):
    url = "http://localhost:8001/api/sesiones/"
    payload = {
        "usuario_id": usuario_id,
        "robot_id": robot_id,
        "fecha_inicio": datetime.now().isoformat()
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            sesion = response.json()
            print(f"Sesión creada: {sesion}")
            return sesion["id"]
        else:
            print("Error al crear sesión:", response.text)
            return None
    except Exception as e:
        print("Error al conectar a la API de sesión:", e)
        return None

def cerrar_sesion_api(sesion_id):
    url = "http://localhost:8001/api/sesiones/cerrar/"
    payload = {
        "sesion_id": sesion_id,
        "fecha_fin": datetime.now().isoformat()
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Sesión cerrada correctamente.")
        else:
            print("Error cerrando sesión:", response.text)
    except Exception as e:
        print("Error al conectar a la API de cerrar sesión:", e)

def modo_chatbot_voz(sesion_id=None):
    intentos_micro = 0
    speak("Dimsor por voz iniciado. Puedes decir 'salir' para terminar o 'sígueme' para iniciar el seguimiento.")
    while True:
        try:
            message = listen()
        except Exception as e:
            intentos_micro += 1
            speak("No se pudo acceder al micrófono. Prueba nuevamente o revisa la conexión del micro.")
            print(f"Error en listen(): {e}")
            if intentos_micro >= 2:
                speak("No fue posible acceder al micrófono. Cambiando al modo texto.")
                print("Cambiando a modo texto automáticamente.")
                modo_chatbot_texto(sesion_id=sesion_id)
                return
            continue
        if not message:
            continue
        if message.lower() in ["salir", "terminar"]:
            speak("Hasta luego.")
            if sesion_id:
                cerrar_sesion_api(sesion_id)
            break
        if comando_seguimiento(message):
            speak("¡Modo seguimiento activado!")
            seguir_persona()
            continue
        ints = predict_class(message)
        if not ints or float(ints[0]['probability']) < 0.4:
            res = retrieval_response(message)
            speak(res)
        else:
            res, tag = get_response(ints)
            speak(res)
            if tag == "realizar prueba":
                pass

def modo_chatbot_texto(sesion_id=None):
    print("Dimsor por texto iniciado. Escribe 'salir' para terminar o 'sígueme' para iniciar el seguimiento.")
    doing_zung = False
    zung_index = 0
    zung_answers = []
    usuario = None
    while True:
        message = input("Tú: ").strip()
        if not message:
            continue
        if message.lower() in ["salir", "terminar"]:
            print("Hasta luego.")
            if sesion_id:
                cerrar_sesion_api(sesion_id)
            break
        if comando_seguimiento(message):
            print("¡Modo seguimiento activado!")
            seguir_persona()
            continue
        if doing_zung:
            preguntas = cargar_preguntas()
            if zung_index == 0:
                usuario = cargar_usuario()
                print(f"Usuario detectado: {usuario}. Responde cada pregunta con: muy pocas veces, algunas veces, muchas veces o casi siempre.")
            if zung_index < len(preguntas):
                pregunta = f"Pregunta {zung_index+1}: {preguntas[zung_index]}"
                print(pregunta)
                answer = message
                if answer.lower() in ["salir", "terminar"]:
                    print("Saliendo de la prueba.")
                    doing_zung = False
                    zung_index = 0
                    zung_answers = []
                    continue
                valor = respuesta_a_valor(answer)
                if valor is not None:
                    zung_answers.append(valor)
                    zung_index += 1
                else:
                    print("Por favor responde con: muy pocas veces, algunas veces, muchas veces o casi siempre.")
                    continue
            else:
                nivel = interpretar_zung(zung_answers)
                print(f"Resultado de la prueba: {nivel}.")
                guardar_resultado(usuario if usuario else "texto", zung_answers, nivel)
                doing_zung = False
                zung_index = 0
                zung_answers = []
                usuario = None
            continue
        if message.lower() in ["mi resultado anterior", "último resultado", "historial"]:
            res, fecha = ultimo_resultado_usuario()
            if res:
                print(f"Tu último resultado fue '{res}' el {fecha}.")
            else:
                print("No tienes resultados guardados todavía.")
            continue
        ints = predict_class(message)
        if not ints or float(ints[0]['probability']) < 0.4:
            res = retrieval_response(message)
            print(res)
        else:
            res, tag = get_response(ints)
            print(res)
            if tag == "realizar prueba":
                doing_zung = True
                zung_index = 0
                zung_answers = []

def obtener_info_usuario(registro_key):
    url = f"http://localhost:8001/api/usuarios/?registro_key={registro_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200 and response.json():
            usuario = response.json()[0]
            return usuario
    except Exception as e:
        print(f"Error obteniendo usuario: {e}")
    return None

def main():
    eyes_thread = threading.Thread(target=mostrar_ojos_robot, daemon=True)
    eyes_thread.start()
    print("Iniciando DIMSOR...")
    reproducir_audio()
    hablar("Iniciando DIMSOR")
    time.sleep(1)

    robot_info = leer_info_local(ROBOT_INFO_FILE)
    if robot_info:
        robot_id = robot_info["id"]
        print(f"Robot ya identificado. ID: {robot_id}")
    else:
        robot_id = registrar_o_verificar_robot()
        print(f"Robot registrado. ID: {robot_id}")

    usuario_data = leer_info_local(USER_SESSION_FILE)
    registro_key = None
    if usuario_data:
        nombre = usuario_data.get("nombre")
        registro_key = usuario_data.get("registro_key")
        rol_id = usuario_data.get("rol_id")
        print(f"Bienvenido de nuevo, {nombre} (registro: {registro_key})")
        hablar(f"Bienvenido de nuevo, {nombre}. ¿Listo para comenzar?")
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
        rol_id = 1
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
                registro_key = registro_key_mostrada
            elif response.status_code == 409:
                try:
                    error_data = response.json()
                    print("Usuario ya registrado:", error_data)
                    hablar("Este usuario ya está registrado. Recuperando información...")
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

    rol_valido = False
    usuario_info = None
    sesion_id = None
    if registro_key:
        usuario_info = obtener_info_usuario(registro_key)
        if usuario_info and usuario_info.get("rol_id") == 3:
            rol_valido = True
        else:
            print("❌ Debes completar tu registro en la página web o en el aplicativo móvil.")
            hablar("Debes completar tu registro en la página web o en el aplicativo móvil antes de continuar.")

    if rol_valido:
        sesion_id = crear_sesion_api(usuario_info["id"], robot_id)
        if sesion_id:
            guardar_info_local({"sesion_id": sesion_id}, SESION_ACTUAL_FILE)
            if verificar_microfono_voz():
                print("🎤 Micrófono detectado. Usando chatbot por voz.")
                modo_chatbot_voz(sesion_id=sesion_id)
            else:
                print("❌ No se detectó micrófono. Usando chatbot por texto.")
                modo_chatbot_texto(sesion_id=sesion_id)
        else:
            print("No se pudo crear la sesión. Contacta soporte.")
            hablar("No se pudo crear la sesión. Por favor intenta más tarde.")
    else:
        print("⛔️ Acceso restringido por rol.")

if __name__ == "__main__":
    main()