import pandas as pd
import joblib
import os
from sklearn.metrics import classification_report, confusion_matrix

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "landmarks_global.csv"))
    model_path = os.path.normpath(os.path.join(script_dir, "..", "..", "models", "abecedario_model.pkl"))

    df = pd.read_csv(data_path)
    if 'partition' not in df.columns:
        print("No existe partición 'valid'.")
        return
    valid_df = df[df['partition'] == 'valid']
    if len(valid_df) == 0:
        print("No hay muestras de validación.")
        return

    X_val = valid_df.drop(['partition', 'clase'], axis=1, errors='ignore')
    y_val = valid_df['clase']

    model = joblib.load(model_path)

    y_pred = model.predict(X_val)

    print(f"Evaluando sobre {len(X_val)} muestras de 'valid'")
    print("Reporte de clasificación:")
    print(classification_report(y_val, y_pred))
    print("Matriz de confusión:")
    print(confusion_matrix(y_val, y_pred))

if __name__ == "__main__":
    main()