import os
import cv2

cap = cv2.VideoCapture(1) 

if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara")
    print("Intentando con diferentes índices de cámara...")
    
    
    for i in range(1, 4):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Cámara encontrada en índice {i}")
            break
    else:
        print("No se encontró ninguna cámara disponible")
        exit()


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

print("Presiona 'q' para salir")

while True:
    
    ret, imagen = cap.read()
    
    if not ret or imagen is None:
        print("Error: No se pudo capturar la imagen")
        continue
    
    if imagen.shape[0] <= 0 or imagen.shape[1] <= 0:
        print("Error: Imagen con dimensiones inválidas")
        continue
    
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    rostros = face_cascade.detectMultiScale(gris, 1.3, 5)
    
    for (x, y, w, h) in rostros:
        cv2.rectangle(imagen, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow('Reconocimiento Facial - Presiona q para salir', imagen)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
cap.release()
cv2.destroyAllWindows()
print("Programa terminado correctamente")