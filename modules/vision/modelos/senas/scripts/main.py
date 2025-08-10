import os
import sys

def run_robotflow_to_csv():
    os.system("python robotflow_a_csv.py")

def run_actualizar_csv():
    os.system("python actualizarcsv.py")

def run_juntar_landmarks():
    os.system("python juntar_landmarks.py")

def run_borrar_imagenes_viejas():
    os.system("python borrar_imagenes_viejas.py")

def run_train_model():
    os.system("python train_model.py")

def run_predict_abecedario():
    os.system("python predict_abecedario.py")

def show_menu():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Procesar imágenes de Roboflow a landmarks CSV")
    print("2. Actualizar all_landmarks.csv con nuevos landmarks")
    print("3. Juntar todos los landmarks en un solo CSV (sobreescribe)")
    print("4. Borrar imágenes y CSV individuales (limpieza)")
    print("5. Entrenar modelo de abecedario")
    print("6. Reconocer letra con cámara (predicción en tiempo real)")
    print("7. Salir")
    return input("Selecciona opción (1-7): ")

if __name__ == "__main__":
    while True:
        opcion = show_menu()
        if opcion == "1":
            run_robotflow_to_csv()
        elif opcion == "2":
            run_actualizar_csv()
        elif opcion == "3":
            run_juntar_landmarks()
        elif opcion == "4":
            run_borrar_imagenes_viejas()
        elif opcion == "5":
            run_train_model()
        elif opcion == "6":
            run_predict_abecedario()
        elif opcion == "7":
            print("¡Saliendo!")
            sys.exit(0)
        else:
            print("Opción no válida, intenta de nuevo.")