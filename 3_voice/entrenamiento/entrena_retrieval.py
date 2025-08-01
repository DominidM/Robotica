import json
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Carga dataset de pares pregunta-respuesta
with open(os.path.join(DATA_DIR, "dialogs_dataset.json"), encoding="utf-8") as f:
    pairs = json.load(f)

questions = [pair["input"] for pair in pairs]
answers = [pair["output"] for pair in pairs]

# Entrena el vectorizador TF-IDF
vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
X = vectorizer.fit_transform(questions)

# Guarda el vectorizador y las respuestas
with open(os.path.join(DATA_DIR, "retrieval_vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)
with open(os.path.join(DATA_DIR, "retrieval_answers.pkl"), "wb") as f:
    pickle.dump(answers, f)

print("Entrenamiento retrieval completado y modelos guardados en /data")