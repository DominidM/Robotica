import pandas as pd
import joblib
import os
import sys

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.normpath(os.path.join(script_dir, "..", "..", "models", "abecedario_model.pkl"))
    model = joblib.load(model_path)

    # Puedes pasar por argumento el archivo CSV de landmarks de una imagen
    if len(sys.argv) < 2:
        print("Uso: python predict_abecedario.py <archivo_landmarks.csv>")
        return
    input_csv = sys.argv[1]
    df = pd.read_csv(input_csv, header=None)
    X = df.values.reshape(1, -1)
    pred = model.predict(X)[0]
    print(f"Predicción: {pred}")

if __name__ == "__main__":
    main()