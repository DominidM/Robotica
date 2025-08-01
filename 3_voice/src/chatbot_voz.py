import speech_recognition as sr
import pyttsx3
from chatbot_core import (
    predict_class,
    get_response,
    retrieval_response,
    zung_questions,
    respuesta_a_valor,
    interpretar_zung,
)

r = sr.Recognizer()

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
    with sr.Microphone() as source:
        print("Habla ahora...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
        try:
            text = r.recognize_google(audio, language="es-ES")
            print("Tú dijiste:", text)
            return text
        except:
            speak("No entendí. Por favor, repite.")
            return ""

doing_zung = False
zung_index = 0
zung_answers = []
first_turn = True

speak("Dimsor por voz iniciado. Puedes decir 'salir' para terminar.")
while True:
    if doing_zung:
        if zung_index == 0:
            speak("Responde cada pregunta con: muy pocas veces, algunas veces, muchas veces o casi siempre.")
        if zung_index < len(zung_questions):
            pregunta = f"Pregunta {zung_index+1}: {zung_questions[zung_index]}"
            speak(pregunta)
            answer = listen()
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
            doing_zung = False
            zung_index = 0
            zung_answers = []
    else:
        if first_turn:
            speak("¿En qué puedo ayudarte?")
            first_turn = False
        message = listen()
        if not message:
            continue
        if message.lower() in ["salir", "terminar"]:
            speak("Hasta luego.")
            break
        ints = predict_class(message)
        # Lógica híbrida: retrieval si intent es poco claro o baja probabilidad
        if not ints or float(ints[0]['probability']) < 0.4:
            res = retrieval_response(message)
            speak(res)
        else:
            res, tag = get_response(ints)
            # Si el intent es saludo, solo responde el saludo una vez, luego responde otra cosa
            if tag == "saludo" and not first_turn:
                # No repetir saludo, buscar otra respuesta neutra
                speak("¿Quieres hablar de algún tema en especial o necesitas ayuda con algo más?")
            else:
                speak(res)
            if tag == "realizar prueba":
                doing_zung = True
                zung_index = 0
                zung_answers = []