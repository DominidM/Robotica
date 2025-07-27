import openai
import speech_recognition as sr
import pyttsx3

# ----------------- CONFIGURACIÓN -----------------
# Pon tu clave de API de OpenAI aquí
openai.api_key = "TU_API_KEY_AQUI"  # <--- REEMPLAZA ESTO

# Opcional: puedes poner el modelo que tengas disponible
OPENAI_MODEL = "gpt-3.5-turbo"

r = sr.Recognizer()

def speak(text):
    try:
        print("Dimsor:", text)
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        del engine
    except Exception as e:
        print("Error en speak:", e)
        print(f"[TTS FALLÓ] Dimsor: {text}")

def listen():
    with sr.Microphone() as source:
        print("Habla ahora...")
        try:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            text = r.recognize_google(audio, language="es-ES")
            print("Tú dijiste:", text)
            return text
        except sr.WaitTimeoutError:
            print("No detecté voz. Intenta de nuevo.")
            speak("No detecté voz. Intenta de nuevo.")
            return ""
        except sr.UnknownValueError:
            print("No entendí. Por favor, repite.")
            speak("No entendí. Por favor, repite.")
            return ""
        except Exception as e:
            print("Error:", e)
            speak("Ocurrió un error. Por favor, repite.")
            return ""

def preguntar_a_gpt(mensaje_usuario):
    try:
        respuesta = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Eres un asistente conversacional por voz, amable y útil, responde en español."},
                {"role": "user", "content": mensaje_usuario}
            ]
        )
        return respuesta.choices[0].message['content']
    except Exception as e:
        print("Error al conectar con OpenAI:", e)
        return "No pude conectar con la inteligencia artificial en este momento."

def main():
    speak("Dimsor por voz con ChatGPT iniciado. Di 'salir' para terminar.")
    while True:
        try:
            speak("¿En qué puedo ayudarte?")
            message = listen()
            if not message:
                continue
            if message.lower() in ["salir", "terminar"]:
                speak("Hasta luego. Recuerda que puedes volver cuando quieras.")
                break
            respuesta = preguntar_a_gpt(message)
            speak(respuesta)
        except KeyboardInterrupt:
            speak("Programa interrumpido. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error en el bucle principal: {e}")
            speak("Ocurrió un error. Continuemos.")

if __name__ == "__main__":
    main()