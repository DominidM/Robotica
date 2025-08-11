import pandas as pd
import joblib
import os
from sklearn.metrics import classification_report, confusion_matrix

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "landmarks_global.csv"))
    model_path = os.path.normpath(os.path.join(script_dir, "..", "..", "models", "abecedario_model.pkl"))
    df = pd.read_csv(data_path)
    # Evalúa sobre 'valid' si existe, si no sobre todo el dataset
    if 'partition' in df.columns:
        eval_df = df[df['partition'] == 'valid']
    else:
        eval_df = df
    X = eval_df.drop(['partition', 'clase'], axis=1, errors='ignore')
    y = eval_df['clase']
    model = joblib.load(model_path)
    y_pred = model.predict(X)
    print("Reporte de clasificación:\n", classification_report(y, y_pred))
    print("Matriz de confusión:\n", confusion_matrix(y, y_pred))

if __name__ == "__main__":
    main()