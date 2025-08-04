import requests
import uuid
import pyttsx3
import time
import pygame
import os
import speech_recognition as sr

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
        
        # Pausa para liberar recursos de audio
        time.sleep(1)
            
    except Exception as e:
        print(f"Error reproduciendo audio: {e}")

def hablar(texto):
    """Función para hablar que reinicializa el motor cada vez"""
    try:
        print(f"🔊 Intentando decir: {texto}")
        
        # Crear nuevo motor cada vez
        engine = pyttsx3.init()
        
        # Configurar propiedades
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        # Hablar
        engine.say(texto)
        engine.runAndWait()
        
        # Limpiar
        engine.stop()
        del engine
        
        # Pequeña pausa
        time.sleep(0.5)
        
        print("✅ Audio completado")
        
    except Exception as e:
        print(f"❌ Error al hablar: {e}")
        print(f"Texto que no se pudo decir: {texto}")

def verificar_microfono():
    """Verifica si hay micrófono disponible"""
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        
        # Buscar dispositivos de entrada
        input_devices = []
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append((i, device_info['name']))
        
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
    """Función para escuchar el nombre del usuario con timeout de 20 segundos"""
    try:
        # Verificar si hay micrófono disponible
        if not verificar_microfono():
            print("❌ No hay micrófono disponible, usando entrada de texto")
            return None
            
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        print("🎤 Preparando micrófono...")
        
        # Ajustar para ruido ambiente
        with microphone as source:
            print("🎤 Calibrando micrófono para ruido ambiente...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
        
        print("🎤 Escuchando nombre... (20 segundos)")
        with microphone as source:
            # Escuchar con timeout de 20 segundos
            audio = recognizer.listen(source, timeout=20, phrase_time_limit=10)
        
        print("🎤 Procesando audio...")
        # Reconocer usando Google (requiere internet)
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
    except OSError as e:
        print(f"❌ Error de dispositivo de audio: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado al escuchar: {e}")
        return None

def confirmar_nombre(nombre):
    """Función para confirmar si el nombre es correcto"""
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    try:
        print("🎤 Escuchando confirmación... (10 segundos)")
        with microphone as source:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        
        print("🎤 Procesando confirmación...")
        respuesta = recognizer.recognize_google(audio, language='es-ES').lower()
        print(f"✅ Respuesta reconocida: {respuesta}")
        
        # Verificar si es afirmativo
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

# --- Inicia DIMSOR ---
print("Iniciando DIMSOR...")

# Reproducir audio de inicio primero
reproducir_audio()

# Continuar con el programa
hablar("Iniciando DIMSOR")

time.sleep(1)
saludo = "Hola, soy Dimsor"
print(saludo)
hablar(saludo)

# --- Pregunta nombre con reconocimiento de voz ---
nombre_confirmado = False
nombre = None
usa_microfono = verificar_microfono()

while not nombre_confirmado:
    pregunta = "¿Cómo te llamas?"
    print(pregunta)
    hablar(pregunta)
    
    if usa_microfono:
        # Intentar usar reconocimiento de voz
        nombre = escuchar_nombre()
        
        if nombre is None:
            disculpa = "No escuché nada, disculpame. Puedes escribir tu nombre:"
            print(disculpa)
            hablar(disculpa)
            nombre = input("Escribe tu nombre: ").strip()
    else:
        # Usar entrada de texto directamente
        hablar("Por favor, escribe tu nombre")
        nombre = input("Escribe tu nombre: ").strip()
    
    if not nombre:
        print("No ingresaste ningún nombre. Intentemos de nuevo.")
        continue
    
    # Confirmar el nombre
    confirmacion = f"Entendí que tu nombre es {nombre}. ¿Es correcto?"
    print(confirmacion)
    hablar(confirmacion)
    
    # Escuchar confirmación o usar texto
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
        confirmado_msg = f"Perfecto, {nombre}. Procedo a registrarte."
        print(confirmado_msg)
        hablar(confirmado_msg)
        nombre_confirmado = True
    else:
        reintentar = "Entiendo, vamos a intentarlo de nuevo."
        print(reintentar)
        hablar(reintentar)

# --- Proceder con el registro en la API ---
registro_key = str(uuid.uuid4())
rol_id = 1  # invitado

payload = {
    "nombre": nombre,
    "registro_key": registro_key,
    "rol_id": rol_id
}

# Para desarrollo en local
url_api = "http://localhost:8000/api/usuarios/"
# Para producción:
# url_api = "https://tu-backend.azurewebsites.net/api/usuarios/"

try:
    response = requests.post(url_api, json=payload)
    
    if response.status_code == 201:
        msg = f"Usuario {nombre} registrado correctamente. Tu código de registro es: {registro_key}"
        print(msg)
        hablar(f"Usuario {nombre} registrado correctamente. Tu código de registro ha sido generado.")
    else:
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