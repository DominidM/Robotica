import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Ruta al CSV unificado (usa ruta absoluta)
csv_path = "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/dataset/all_landmarks.csv"
model_path = "C:/Users/ASKINET/Desktop/REPOSITORIES/Robotica/modules/vision/modelos/senas/models/abecedario_model.pkl"

# Leer el CSV unificado
df = pd.read_csv(csv_path)

# Extraer features (landmarks) y labels
X = df.drop(['label', 'image'], axis=1).values
y = df['label'].values

if len(X) == 0 or len(y) == 0:
    raise ValueError("No se encontraron datos en all_landmarks.csv. Verifica que el archivo tenga filas y columnas.")

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, model_path)
print(f"Modelo de abecedario entrenado y guardado en {model_path}.")