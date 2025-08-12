import pandas as pd
import joblib
import os
from sklearn.metrics import classification_report, confusion_matrix

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "landmarks_global.csv"))
    model_path = os.path.normpath(os.path.join(script_dir, "..", "..", "models", "abecedario_model.pkl"))
    df = pd.read_csv(data_path)
    # Evalúa sobre 'valid' si existe y tiene datos, si no sobre todo el dataset
    if 'partition' in df.columns and (df['partition'] == 'valid').any():
        eval_df = df[df['partition'] == 'valid']
        print(f"Evaluando sobre {len(eval_df)} muestras de 'valid'")
    else:
        eval_df = df
        print(f"No hay partición 'valid'. Evaluando sobre todo el dataset ({len(eval_df)} muestras)")
    X = eval_df.drop(['partition', 'clase'], axis=1, errors='ignore')
    y = eval_df['clase']
    if len(X) == 0:
        print("No hay muestras para evaluar. Revisa tu CSV.")
        return
    model = joblib.load(model_path)
    y_pred = model.predict(X)
    print("Reporte de clasificación:\n", classification_report(y, y_pred))
    print("Matriz de confusión:\n", confusion_matrix(y, y_pred))

if __name__ == "__main__":
    main()