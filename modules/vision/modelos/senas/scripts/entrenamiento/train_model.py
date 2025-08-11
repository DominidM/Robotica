import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "landmarks_global.csv"))
    df = pd.read_csv(data_path)
    # Usa solo 'train' si existe la columna partition
    if 'partition' in df.columns:
        train_df = df[df['partition'] == 'train']
    else:
        train_df = df
    X = train_df.drop(['partition', 'clase'], axis=1, errors='ignore')
    y = train_df['clase']
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.15, random_state=42)
    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(X_train, y_train)
    print("Score validación:", model.score(X_val, y_val))
    model_path = os.path.normpath(os.path.join(script_dir, "..", "..", "models", "abecedario_model.pkl"))
    joblib.dump(model, model_path)
    print("Modelo guardado en", model_path)

if __name__ == "__main__":
    main()