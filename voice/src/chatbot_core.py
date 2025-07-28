import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
lemmatizer = WordNetLemmatizer()

# Carga modelos y datos
intents = json.load(open(os.path.join(DATA_DIR, 'intents.json'), encoding="utf-8"))
words = pickle.load(open(os.path.join(DATA_DIR, 'words.pkl'), 'rb'))
classes = pickle.load(open(os.path.join(DATA_DIR, 'classes.pkl'), 'rb'))
model = load_model(os.path.join(DATA_DIR, 'chatbot_model.h5'))

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

def get_response(ints):
    if len(ints) == 0:
        return "No entiendo, ¿puedes reformular?", None
    tag = ints[0]['intent']
    for i in intents['intents']:
        if i['tag'] == tag:
            return np.random.choice(i['responses']), tag
    return "No entiendo, ¿puedes reformular?", tag

# Test clínico (Zung)
def cargar_preguntas_zung():
    # Puedes cargar de JSON externo, o definir aquí
    return [
        "Me siento triste y deprimido.",
        "Por las mañanas me siento mejor que por las tardes.",
        # ... resto de preguntas ...
    ]

zung_questions = cargar_preguntas_zung()
text_to_score = {
    1: ["muy pocas veces", "nunca", "casi nunca", "nada", "jamás", "ninguna vez", "para nada", "raramente", "pocas veces"],
    2: ["algunas veces", "a veces", "ocasionalmente", "poco", "de vez en cuando"],
    3: ["muchas veces", "frecuentemente", "a menudo", "bastante", "seguido", "considerablemente"],
    4: ["casi siempre", "siempre", "todo el tiempo", "la mayoría de las veces", "muy frecuente"]
}
zung_reverse = {4:1, 3:2, 2:3, 1:4}
zung_reverse_questions = [2, 5, 6, 11, 12, 14, 16, 17, 18, 20]

def respuesta_a_valor(texto):
    texto = texto.strip().lower()
    for val, palabras in text_to_score.items():
        for palabra in palabras:
            if palabra in texto:
                return val
    if texto in ["1", "2", "3", "4"]:
        return int(texto)
    return None

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