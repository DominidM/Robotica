import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import joblib
import os
import sys

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "landmarks_global.csv"))
    model_path = os.path.normpath(os.path.join(script_dir, "..", "..", "models", "abecedario_model.pkl"))
    score_path = os.path.normpath(os.path.join(script_dir, "..", "..", "models", "score.txt"))

    df = pd.read_csv(data_path)
    
    # Usa solo 'train' si existe la columna partition
    if 'partition' in df.columns:
        train_df = df[df['partition'] == 'train']
        valid_df = df[df['partition'] == 'valid']
        print(f"Entrenando con {len(train_df)} muestras, validando con {len(valid_df)} muestras.")
    else:
        train_df = df
        valid_df = None
        print(f"Entrenando con todo el dataset ({len(train_df)} muestras). No hay partición 'valid'.")

    X_train = train_df.drop(['partition', 'clase'], axis=1, errors='ignore')
    y_train = train_df['clase']

    # Validación externa si existe
    if valid_df is not None and len(valid_df) > 0:
        X_val = valid_df.drop(['partition', 'clase'], axis=1, errors='ignore')
        y_val = valid_df['clase']
    else:
        X_val = None
        y_val = None

    # Permite elegir modelo por parámetro (por defecto RandomForest)
    use_rf = True
    if len(sys.argv) > 1 and sys.argv[1].lower() == "logistic":
        use_rf = False

    if use_rf:
        model = RandomForestClassifier(n_estimators=150, random_state=42)
        print("Modelo: RandomForestClassifier")
    else:
        model = LogisticRegression(max_iter=1000, random_state=42)
        print("Modelo: LogisticRegression")

    model.fit(X_train, y_train)

    # Validación externa si existe
    if X_val is not None and y_val is not None and len(X_val) > 0:
        score = model.score(X_val, y_val)
        print(f"Score en validación externa: {score:.3f}")
    else:
        score = model.score(X_train, y_train)
        print(f"Score en entrenamiento: {score:.3f}")

    # Guarda el modelo entrenado
    joblib.dump(model, model_path)
    print(f"Modelo guardado en {model_path}")

    # Guarda el score en un archivo de texto
    with open(score_path, "w") as fscore:
        fscore.write(f"Score: {score:.3f}\n")

if __name__ == "__main__":
    main()