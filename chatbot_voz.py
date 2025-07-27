import random
import json
import pickle
import numpy as np
import speech_recognition as sr
import pyttsx3
from keras.models import load_model
import nltk
from nltk.stem import WordNetLemmatizer

# Inicializa voz a texto y texto a voz
r = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print("Dimsor (habla):", text)
    engine.say(text)
    engine.runAndWait()

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json', encoding="utf-8").read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

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
        return "No entiendo, ¿puedes repetir?"
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "No entiendo, ¿puedes repetir?"

print("Dimsor Chatbot por voz iniciado! Di 'salir' para terminar.")

while True:
    try:
        with sr.Microphone() as source:
            print("Habla ahora...")
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio, language="es-ES")
            print("Tú dijiste:", text)
            if text.lower() == "salir":
                speak("¡Hasta luego!")
                break
            ints = predict_class(text)
            res = get_response(ints, intents)
            speak(res)
    except sr.WaitTimeoutError:
        print("No detecté voz. Intenta de nuevo.")
    except sr.UnknownValueError:
        print("No entendí. Por favor, repite.")
    except Exception as e:
        print("Error:", e)