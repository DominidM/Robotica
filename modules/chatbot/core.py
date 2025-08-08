import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import os
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "chatbot/data")

lemmatizer = WordNetLemmatizer()

# Carga intents y datos del chatbot
intents = json.load(open(os.path.join(DATA_DIR, 'intents.json'), encoding="utf-8"))
words = pickle.load(open(os.path.join(DATA_DIR, 'words.pkl'), 'rb'))
classes = pickle.load(open(os.path.join(DATA_DIR, 'classes.pkl'), 'rb'))
model = load_model(os.path.join(DATA_DIR, 'chatbot_model.h5'))

# Retrieval QA
try:
    with open(os.path.join(DATA_DIR, "retrieval_vectorizer.pkl"), "rb") as f:
        retrieval_vectorizer = pickle.load(f)
    with open(os.path.join(DATA_DIR, "retrieval_answers.pkl"), "rb") as f:
        retrieval_answers = pickle.load(f)
    with open(os.path.join(DATA_DIR, "dialogs_dataset.json"), encoding="utf-8") as f:
        retrieval_pairs = json.load(f)
    retrieval_questions = [pair["input"] for pair in retrieval_pairs]
    def retrieval_response(user_input, threshold=0.3):
        X_input = retrieval_vectorizer.transform([user_input])
        questions_matrix = retrieval_vectorizer.transform(retrieval_questions)
        similarities = cosine_similarity(X_input, questions_matrix)
        best_idx = similarities.argmax()
        best_score = similarities[0, best_idx]
        if best_score < threshold:
            return "No encontré una respuesta adecuada. ¿Puedes reformular tu pregunta?"
        return retrieval_answers[best_idx]
except Exception as e:
    print("Retrieval no disponible:", e)
    def retrieval_response(user_input, threshold=0.3):
        return "Funcionalidad de retrieval no disponible."

# Funciones de procesamiento de intents
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
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