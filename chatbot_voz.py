import random
import json
import pickle
import numpy as np
import speech_recognition as sr
import pyttsx3
from keras.models import load_model
import nltk
from nltk.stem import WordNetLemmatizer

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

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json', encoding="utf-8").read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

zung_questions = [
    "Me siento triste y deprimido.",
    "Por las mañanas me siento mejor que por las tardes.",
    "Frecuentemente tengo ganas de llorar y a veces lloro.",
    "Me cuesta mucho dormir o duermo mal por las noches.",
    "Ahora tengo tanto apetito como antes.",
    "Todavía me siento atraído por el sexo opuesto.",
    "Creo que estoy adelgazando.",
    "Estoy estreñido.",
    "Tengo palpitaciones.",
    "Me canso por cualquier cosa.",
    "Mi cabeza está tan despejada como antes.",
    "Hago las cosas con la misma facilidad que antes.",
    "Me siento agitado e intranquilo y no puedo estar quieto.",
    "Tengo esperanza y confío en el futuro.",
    "Me siento más irritable que habitualmente.",
    "Encuentro fácil tomar decisiones.",
    "Me creo útil y necesario para la gente.",
    "Encuentro agradable vivir, mi vida es plena.",
    "Creo que sería mejor para los demás si me muriera.",
    "Me gustan las mismas cosas que solían agradarme."
]

# Mapear texto a puntaje
text_to_score = {
    1: ["muy pocas veces", "nunca", "casi nunca", "nada", "jamás", "ninguna vez", "para nada", "raramente", "pocas veces"],
    2: ["algunas veces", "a veces", "ocasionalmente", "poco", "de vez en cuando"],
    3: ["muchas veces", "frecuentemente", "a menudo", "bastante", "seguido", "considerablemente"],
    4: ["casi siempre", "siempre", "todo el tiempo", "la mayoría de las veces", "muy frecuente"]
}

def respuesta_a_valor(texto):
    texto = texto.strip().lower()
    for val, palabras in text_to_score.items():
        for palabra in palabras:
            if palabra in texto:
                return val
    # Si el usuario responde solo con números
    if texto in ["1", "2", "3", "4"]:
        return int(texto)
    # Si no se reconoce, pedir repetir
    return None

zung_reverse = {4:1, 3:2, 2:3, 1:4}
zung_reverse_questions = [2, 5, 6, 11, 12, 14, 16, 17, 18, 20]

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    p = bow(sentence, words)
    res = model.predict(np.array([p]), verbose=0)[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(ints, intents_json):
    if len(ints) == 0:
        return "No entiendo, ¿puedes reformular?"
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "No entiendo, ¿puedes reformular?"

def interpretar_zung(respuestas):
    puntaje = 0
    for idx, r in enumerate(respuestas):
        valor = r
        if (idx+1) in zung_reverse_questions:
            valor = zung_reverse.get(valor, valor)
        puntaje += valor
    if puntaje <= 28:
        nivel = "Ausencia de depresión"
    elif 29 <= puntaje <= 41:
        nivel = "Depresión leve"
    elif 42 <= puntaje <= 53:
        nivel = "Depresión moderada"
    else:
        nivel = "Depresión grave"
    return nivel

def main():
    speak("Dimsor por voz iniciado. Di 'salir' para terminar.")
    doing_zung = False
    zung_index = 0
    zung_answers = []

    while True:
        try:
            if doing_zung:
                if zung_index == 0:
                    speak("Responde cada pregunta con palabras como: muy pocas veces, algunas veces, muchas veces o casi siempre.")
                if zung_index < len(zung_questions):
                    pregunta = f"Pregunta {zung_index+1}: {zung_questions[zung_index]}"
                    speak(pregunta)
                    while True:
                        answer = listen()
                        if answer.lower() in ["salir", "terminar"]:
                            speak("Saliendo de la prueba. Recuerda que siempre estaré aquí para escucharte y apoyarte.")
                            doing_zung = False
                            zung_index = 0
                            zung_answers = []
                            break
                        valor = respuesta_a_valor(answer)
                        if valor is not None:
                            zung_answers.append(valor)
                            zung_index += 1
                            break
                        elif not answer:
                            continue
                        else:
                            speak("Por favor, responde con: muy pocas veces, algunas veces, muchas veces o casi siempre.")
                else:
                    speak("¡Has terminado la prueba de Zung! Gracias por tus respuestas.")
                    nivel = interpretar_zung(zung_answers)
                    speak(f"Resultado de la prueba: {nivel}.")
                    speak("Recuerda que siempre estaré aquí para escucharte y apoyarte.")
                    doing_zung = False
                    zung_index = 0
                    zung_answers = []
            else:
                speak("¿En qué puedo ayudarte?")
                message = listen()
                if not message:
                    continue
                if message.lower() in ["salir", "terminar"]:
                    speak("Hasta luego. Recuerda que puedes volver cuando quieras.")
                    break
                ints = predict_class(message)
                res = get_response(ints, intents)
                speak(res)
                if ints and ints[0]['intent'] == "realizar prueba":
                    doing_zung = True
                    zung_index = 0
                    zung_answers = []
        except KeyboardInterrupt:
            speak("Programa interrumpido. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error en el bucle principal: {e}")
            speak("Ocurrió un error. Continuemos.")

if __name__ == "__main__":
    main()