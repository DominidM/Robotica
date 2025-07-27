import random
import json
import pickle
import numpy as np
from keras.models import load_model
import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json', encoding="utf-8").read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

zung_questions = [
    "Me siento decaído y triste.",
    "Por las mañanas es cuando me siento mejor.",
    "Lloro o siento ganas de llorar.",
    "Tengo problemas para dormir por la noche.",
    "Como igual que antes.",
    "Disfruto de las cosas igual que antes.",
    "He notado una pérdida de peso.",
    "Tengo problemas de estreñimiento.",
    "El corazón me late más deprisa de lo habitual.",
    "Me canso sin razón.",
    # ... hasta 20 preguntas
]

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

print("Dimsor Chatbot iniciado! (escribe 'salir' para terminar)")
doing_zung = False
zung_index = 0
zung_answers = []

while True:
    if doing_zung:
        if zung_index < len(zung_questions):
            print(f"Pregunta {zung_index+1}: {zung_questions[zung_index]}")
            answer = input("Tu respuesta (nunca, a veces, frecuentemente, siempre): ")
            zung_answers.append(answer.lower())
            zung_index += 1
        else:
            print("¡Has terminado la prueba de Zung! Gracias por tus respuestas.")
            # Aquí puedes analizar las respuestas y dar un mensaje personalizado
            print("Recuerda que siempre estaré aquí para escucharte y apoyarte.")
            doing_zung = False
            zung_index = 0
            zung_answers = []
    else:
        message = input("")
        if message.lower() == "salir":
            break
        ints = predict_class(message)
        res = get_response(ints, intents)
        print(res)
        # Detectar si el intent es 'realizar prueba'
        if ints and ints[0]['intent'] == "realizar prueba":
            doing_zung = True
            zung_index = 0
            zung_answers = []