import speech_recognition as sr
import pyttsx3

from modules.chatbot.core import (
    predict_class,
    get_response,
    retrieval_response,
)
from modules.test_psico.test_zung import (
    cargar_preguntas,
    respuesta_a_valor,
    interpretar_zung,
    guardar_resultado,
    cargar_usuario,
    ultimo_resultado_usuario,
)

r = sr.Recognizer()

def verificar_microfono_voz():
    try:
        mic_list = sr.Microphone.list_microphone_names()
        if not mic_list:
            print("❌ No se detectó ningún micrófono.")
            return False
        print(f"Micrófonos detectados: {mic_list}")
        return True
    except Exception as e:
        print(f"Error verificando micrófono: {e}")
        return False

def speak(text):
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

def listen():
    try:
        with sr.Microphone() as source:
            print("Habla ahora...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            try:
                text = r.recognize_google(audio, language="es-ES")
                print("Tú dijiste:", text)
                return text
            except sr.UnknownValueError:
                speak("No entendí. Por favor, repite.")
                return ""
            except sr.RequestError as e:
                speak("Error con el servicio de reconocimiento. Revisa tu conexión.")
                return ""
    except OSError as e:
        print(f"Error en listen(): {e}")
        raise
    except Exception as e:
        print(f"Error en listen(): {e}")
        raise

def iniciar_chatbot_voz():
    if not verificar_microfono_voz():
        speak("No se detectó micrófono. No puedes usar el modo voz en este equipo.")
        input("Presiona Enter para volver al menú...")
        return

    doing_zung = False
    zung_index = 0
    zung_answers = []
    first_turn = True
    usuario = None

    speak("Dimsor por voz iniciado. Puedes decir 'salir' para terminar.")
    while True:
        if doing_zung:
            preguntas = cargar_preguntas()
            if zung_index == 0:
                usuario = cargar_usuario()
                speak(f"Usuario detectado: {usuario}. Responde cada pregunta con: muy pocas veces, algunas veces, muchas veces o casi siempre.")
            if zung_index < len(preguntas):
                pregunta = f"Pregunta {zung_index+1}: {preguntas[zung_index]}"
                speak(pregunta)
                try:
                    answer = listen()
                except Exception as e:
                    speak("No se pudo acceder al micrófono. Cancelando modo voz.")
                    print(f"Error en listen(): {e}")
                    return
                if answer.lower() in ["salir", "terminar"]:
                    speak("Saliendo de la prueba.")
                    doing_zung = False
                    zung_index = 0
                    zung_answers = []
                    continue
                valor = respuesta_a_valor(answer)
                if valor is not None:
                    zung_answers.append(valor)
                    zung_index += 1
                else:
                    speak("Por favor responde con: muy pocas veces, algunas veces, muchas veces o casi siempre.")
                    continue
            else:
                nivel = interpretar_zung(zung_answers)
                speak(f"Resultado de la prueba: {nivel}.")
                guardar_resultado(usuario if usuario else "voz", zung_answers, nivel)
                doing_zung = False
                zung_index = 0
                zung_answers = []
                usuario = None
        else:
            if first_turn:
                speak("¿En qué puedo ayudarte?")
                first_turn = False
            try:
                message = listen()
            except Exception as e:
                speak("No se pudo acceder al micrófono. Cancelando modo voz.")
                print(f"Error en listen(): {e}")
                return
            if not message:
                continue
            if message.lower() in ["salir", "terminar"]:
                speak("Hasta luego.")
                break
            if message.lower() in ["mi resultado anterior", "último resultado", "historial"]:
                res, fecha = ultimo_resultado_usuario()
                if res:
                    speak(f"Tu último resultado fue '{res}' el {fecha}.")
                else:
                    speak("No tienes resultados guardados todavía.")
                continue
            ints = predict_class(message)
            if not ints or float(ints[0]['probability']) < 0.4:
                res = retrieval_response(message)
                speak(res)
            else:
                res, tag = get_response(ints)
                if tag == "saludo" and not first_turn:
                    speak("¿Quieres hablar de algún tema en especial o necesitas ayuda con algo más?")
                else:
                    speak(res)
                if tag == "realizar prueba":
                    doing_zung = True
                    zung_index = 0
                    zung_answers = []

if __name__ == "__main__":
    iniciar_chatbot_voz()