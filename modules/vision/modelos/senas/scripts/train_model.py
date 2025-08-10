#entrenamiento
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data_dir = "../dataset/landmarks"
X, y = [], []

for letter in os.listdir(data_dir):
    letter_dir = os.path.join(data_dir, letter)
    if os.path.isdir(letter_dir):
        for file in os.listdir(letter_dir):
            if file.endswith('.csv'):
                df = pd.read_csv(os.path.join(letter_dir, file))
                # Extrae todos los landmarks (x, y, z) en una lista plana
                features = []
                for i in range(len(df)):
                    features.extend([df.loc[i, "x"], df.loc[i, "y"], df.loc[i, "z"]])
                X.append(features)
                y.append(letter)

X = np.array(X)
y = np.array(y)

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)
joblib.dump(model, "../models/abecedario_model.pkl")
print("Modelo de abecedario entrenado y guardado.")