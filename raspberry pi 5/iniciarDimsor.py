import requests
import pyttsx3
import time
import pygame
import os
import speech_recognition as sr
import random
import string

def reproducir_audio():
    """Reproduce audio y libera recursos completamente"""
    try:
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        audio_file = os.path.join(script_dir, 'sonido_inicio.mp3')
        
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        # Esperar a que termine
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        time.sleep(1)
    except Exception as e:
        print(f"Error reproduciendo audio: {e}")

def hablar(texto):
    """Función para hablar que reinicializa el motor cada vez"""
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

def verificar_microfono():
    """Verifica si hay micrófono disponible"""
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        input_devices = [
            (i, audio.get_device_info_by_index(i)['name'])
            for i in range(audio.get_device_count())
            if audio.get_device_info_by_index(i)['maxInputChannels'] > 0
        ]
        audio.terminate()
        if input_devices:
            print(f"✅ Dispositivos de entrada encontrados: {len(input_devices)}")
            for idx, name in input_devices:
                print(f"  - {idx}: {name}")
            return True
        else:
            print("❌ No se encontraron dispositivos de entrada")
            return False
    except Exception as e:
        print(f"❌ Error verificando micrófono: {e}")
        return False

def escuchar_nombre():
    """Escucha el nombre del usuario por voz, con timeout"""
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
        print("🎤 Escuchando nombre... (20 segundos)")
        with microphone as source:
            audio = recognizer.listen(source, timeout=20, phrase_time_limit=10)
        print("🎤 Procesando audio...")
        nombre = recognizer.recognize_google(audio, language='es-ES')
        print(f"✅ Nombre reconocido: {nombre}")
        return nombre.strip()
    except sr.WaitTimeoutError:
        print("⏰ Timeout: No se escuchó nada en 20 segundos")
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
    """Confirma si el nombre escuchado es correcto"""
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    try:
        print("🎤 Escuchando confirmación... (10 segundos)")
        with microphone as source:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        print("🎤 Procesando confirmación...")
        respuesta = recognizer.recognize_google(audio, language='es-ES').lower()
        print(f"✅ Respuesta reconocida: {respuesta}")
        palabras_si = ["sí", "si", "yes", "correcto", "exacto", "afirmativo", "claro"]
        return any(palabra in respuesta for palabra in palabras_si)
    except sr.WaitTimeoutError:
        print("⏰ Timeout en confirmación")
        return False
    except sr.UnknownValueError:
        print("❌ No se pudo entender la confirmación")
        return False
    except Exception as e:
        print(f"❌ Error al confirmar: {e}")
        return False

def generar_registro_key():
    """Genera una clave de registro tipo XXX-XXX-XXX"""
    grupos = []
    for _ in range(3):
        grupo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        grupos.append(grupo)
    return "-".join(grupos)

# --- Inicio DIMSOR ---
print("Iniciando DIMSOR...")
reproducir_audio()
hablar("Iniciando DIMSOR")
time.sleep(1)
print("Hola, soy Dimsor")
hablar("Hola, soy Dimsor")

# --- Pregunta nombre con reconocimiento de voz ---
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

# --- Proceder con el registro en la API ---
registro_key = generar_registro_key()
rol_id = 1  # invitado

payload = {
    "nombre": nombre,
    "registro_key": registro_key,
    "rol_id": rol_id
}

url_api = "http://localhost:8001/api/usuarios/ingresar"
# url_api = "https://tu-backend.azurewebsites.net/api/usuarios/ingresar"

try:
    response = requests.post(url_api, json=payload)
    if response.status_code in (200, 201):
        # Muestra la clave real devuelta por el backend si existe
        data = response.json()
        registro_key_mostrada = data.get("registro_key", registro_key)
        print(f"Usuario {nombre} registrado correctamente. Tu código de registro es: {registro_key_mostrada}")
        hablar(f"Usuario {nombre} registrado correctamente. Tu código de registro es {registro_key_mostrada}")
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