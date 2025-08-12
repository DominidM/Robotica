import pandas as pd
from sklearn.model_selection import train_test_split
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.normpath(os.path.join(script_dir, "..", "..", "dataset", "landmarks_global.csv"))

    df = pd.read_csv(data_path)

    # Si ya existe la columna partition, elimínala para evitar duplicados
    if 'partition' in df.columns:
        print("La columna 'partition' ya existe. Se sobrescribirá.")
        df = df.drop(columns=['partition'])

    # Split en train/valid
    X = df.copy()
    y = df['clase']
    X_train, X_valid = train_test_split(X, test_size=0.15, random_state=42, stratify=y)

    X_train['partition'] = 'train'
    X_valid['partition'] = 'valid'

    df_final = pd.concat([X_train, X_valid], ignore_index=True)
    df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)

    df_final.to_csv(data_path, index=False)
    print(f"Guardado dataset con 'partition' en {data_path}")
    print(df_final['partition'].value_counts())

if __name__ == "__main__":
    main()