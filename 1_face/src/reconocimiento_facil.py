import tensorflow as tf
import cv2
import numpy as np
import os
import time
import pickle
from sklearn.metrics.pairwise import cosine_similarity


DIR_KNOWNS = 'knowns'
DIR_UNKNOWNS = 'unknowns'
DIR_RESULTS = 'results'
DATABASE_FILE = 'face_database.pkl'


for directory in [DIR_KNOWNS, DIR_UNKNOWNS, DIR_RESULTS]:
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_mobilenet_model():
    """Cargar modelo MobileNet para extracción de características"""
    try:
        
        base_model = tf.keras.applications.MobileNetV2(
            weights='imagenet',
            include_top=False,  
            input_shape=(224, 224, 3),
            pooling='avg'  
        )
        print("Modelo MobileNet cargado exitosamente para extracción de características")
        return base_model, "keras_model"
        
    except Exception as e:
        print(f"Error al cargar modelo: {e}")
        return None, None


def preprocess_face_for_mobilenet(face_image, target_size=(224, 224)):
    """Preprocesar rostro para MobileNet"""
    try:
        
        face_resized = cv2.resize(face_image, target_size)
        
        
        if len(face_resized.shape) == 3:
            face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
        else:
            face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_GRAY2RGB)
        
        
        face_array = face_rgb.astype(np.float32)
        face_array = tf.keras.applications.mobilenet_v2.preprocess_input(face_array)
        
        
        face_batch = np.expand_dims(face_array, axis=0)
        
        return face_batch
    except Exception as e:
        print(f"Error en preprocesamiento: {e}")
        return None

def extract_face_features(face_image, model):
    """Extraer características del rostro usando MobileNet"""
    try:
        processed_face = preprocess_face_for_mobilenet(face_image)
        if processed_face is None:
            return None
        
        
        features = model.predict(processed_face, verbose=0)
        return features[0]  
        
    except Exception as e:
        print(f"Error en extracción de características: {e}")
        return None


def load_face_database():
    """Cargar base de datos de rostros conocidos"""
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, 'rb') as f:
                database = pickle.load(f)
            print(f"Base de datos cargada: {len(database)} personas registradas")
            return database
        except:
            print("Error al cargar base de datos, creando nueva")
    
    return {}

def save_face_database(database):
    """Guardar base de datos de rostros"""
    try:
        with open(DATABASE_FILE, 'wb') as f:
            pickle.dump(database, f)
        print("Base de datos guardada exitosamente")
    except Exception as e:
        print(f"Error al guardar base de datos: {e}")

def add_person_to_database(name, face_image, model, database):
    """Agregar nueva persona a la base de datos"""
    features = extract_face_features(face_image, model)
    if features is not None:
        if name not in database:
            database[name] = []
        database[name].append(features)
        print(f"Persona '{name}' agregada a la base de datos")
        return True
    return False

def recognize_face(face_image, model, database, threshold=0.7):
    """Reconocer rostro comparando con base de datos"""
    if not database:
        return "Desconocido", 0.0
    
    
    current_features = extract_face_features(face_image, model)
    if current_features is None:
        return "Error", 0.0
    
    best_match = "Desconocido"
    best_similarity = 0.0
    
    
    for name, person_features_list in database.items():
        for person_features in person_features_list:
            
            similarity = cosine_similarity(
                current_features.reshape(1, -1),
                person_features.reshape(1, -1)
            )[0][0]
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = name
    
    
    if best_similarity >= threshold:
        return best_match, best_similarity
    else:
        return "Desconocido", best_similarity

def train_from_known_faces(model, database):
    """Entrenar base de datos con rostros en la carpeta 'knowns'"""
    print("Entrenando con rostros conocidos...")
    
    if not os.path.exists(DIR_KNOWNS):
        print("Carpeta 'knowns' no encontrada")
        return database
    
    for filename in os.listdir(DIR_KNOWNS):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            
            person_name = os.path.splitext(filename)[0]
            
            
            image_path = os.path.join(DIR_KNOWNS, filename)
            image = cv2.imread(image_path)
            
            if image is not None:
                print(f"Procesando: {person_name}")
            
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                
                if len(faces) > 0:
                    
                    x, y, w, h = faces[0]
                    face = image[y:y+h, x:x+w]
                    add_person_to_database(person_name, face, model, database)
                else:
                    print(f"No se detectó rostro en {filename}")
            else:
                print(f"No se pudo cargar {filename}")
    
    return database


def setup_camera():
    """Configurar y encontrar cámara disponible"""
    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara")
        print("Intentando con diferentes índices de cámara...")
        
        for i in range(4):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"Cámara encontrada en índice {i}")
                break
        else:
            print("No se encontró ninguna cámara disponible")
            return None

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    return cap


def main():
    print("Iniciando reconocimiento facial con nombres...")
    

    print("Cargando modelo MobileNet...")
    model, model_type = load_mobilenet_model()
    if model is None:
        print("Error al cargar el modelo")
        return
    
    
    face_database = load_face_database()
    
    
    face_database = train_from_known_faces(model, face_database)
    save_face_database(face_database)
    
    
    cap = setup_camera()
    if cap is None:
        return
    
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    recognition_interval = 30  
    frame_count = 0
    last_recognitions = {}  
    
    print("Sistema iniciado. Controles:")
    print("- 'q': Salir")
    print("- 's': Guardar rostro como desconocido")
    print("- 'n': Agregar nueva persona (después de presionar 's')")
    print("- 'r': Recargar base de datos")
    print("- 'p': Pausar/reanudar reconocimiento")
    
    recognition_enabled = True
    last_saved_face = None
    
    while True:
        ret, imagen = cap.read()
        
        if not ret or imagen is None:
            print("Error: No se pudo capturar la imagen")
            continue
        
        if imagen.shape[0] <= 0 or imagen.shape[1] <= 0:
            print("Error: Imagen con dimensiones inválidas")
            continue
        
        frame_count += 1
        

        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        

        rostros = face_cascade.detectMultiScale(gris, 1.3, 5)
        
        
        for i, (x, y, w, h) in enumerate(rostros):
            
            color = (0, 255, 0)  
            
            
            rostro = imagen[y:y+h, x:x+w]
            

            if recognition_enabled and frame_count % recognition_interval == 0 and rostro.size > 0:
                name, confidence = recognize_face(rostro, model, face_database)
                last_recognitions[i] = (name, confidence)
                
                
                if name != "Desconocido":
                    if confidence > 0.8:
                        color = (0, 255, 0)    
                    elif confidence > 0.7:
                        color = (0, 255, 255) 
                    else:
                        color = (0, 165, 255)  
                else:
                    color = (0, 0, 255)        
            
            
            cv2.rectangle(imagen, (x, y), (x+w, y+h), color, 2)
            
        
            if i in last_recognitions:
                name, confidence = last_recognitions[i]
                label = f"{name} ({confidence:.2f})"
                
                # Fondo para el texto
                cv2.rectangle(imagen, (x, y-25), (x+w, y), (0, 0, 0), -1)
                cv2.putText(imagen, label, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            else:
                
                cv2.rectangle(imagen, (x, y-25), (x+w, y), (0, 0, 0), -1)
                cv2.putText(imagen, "Analizando...", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        

        info_text = f"Rostros: {len(rostros)} | BD: {len(face_database)} personas | Frame: {frame_count}"
        if not recognition_enabled:
            info_text += " | PAUSADO"
        
        cv2.putText(imagen, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        
        cv2.imshow('Reconocimiento Facial - q:salir s:guardar n:nueva persona r:recargar p:pausar', imagen)
        
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('s') and len(rostros) > 0:
            
            x, y, w, h = rostros[0]
            rostro_guardado = imagen[y:y+h, x:x+w]
            timestamp = int(time.time())
            filename = f"{DIR_UNKNOWNS}/rostro_{timestamp}.jpg"
            cv2.imwrite(filename, rostro_guardado)
            last_saved_face = rostro_guardado
            print(f"Rostro guardado: {filename}")
            print("Presiona 'n' para agregar esta persona a la base de datos")
        elif key == ord('n') and last_saved_face is not None:
            
            name = input("Ingresa el nombre de la persona: ").strip()
            if name:
                if add_person_to_database(name, last_saved_face, model, face_database):
                    save_face_database(face_database)
                    print(f"Persona '{name}' agregada exitosamente")
                    last_saved_face = None
                else:
                    print("Error al agregar persona")
            else:
                print("Nombre inválido")
        elif key == ord('r'):
            
            face_database = load_face_database()
            face_database = train_from_known_faces(model, face_database)
            save_face_database(face_database)
            print("Base de datos recargada")
        elif key == ord('p'):
            recognition_enabled = not recognition_enabled
            status = "habilitado" if recognition_enabled else "pausado"
            print(f"Reconocimiento {status}")
    

    cap.release()
    cv2.destroyAllWindows()
    print("Programa terminado correctamente")


if __name__ == "__main__":
    main()