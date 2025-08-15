import cv2
import mediapipe as mp
import math
from collections import Counter

def detectar_emocion_por_longitudes(longitud1, longitud2, longitud3, longitud4):
    if longitud1 < 19 and longitud2 < 19 and 80 < longitud3 < 95 and longitud4 < 5:
        return 'Enojada'
    elif 20 < longitud1 < 30 and 20 < longitud2 < 30 and longitud3 > 109 and longitud4 > 15:
        return 'Feliz'
    elif longitud1 > 35 and longitud2 > 35 and 80 < longitud3 < 90 and longitud4 > 20:
        return 'Asombrada'
    elif 20 < longitud1 < 35 and 20 < longitud2 < 35 and 80 < longitud3 < 100:
        return 'Triste'
    return "Desconocido"

def detectar_emocion_predominante(num_frames=10, cam_index=0, mostrar=True):
    cap = cv2.VideoCapture(cam_index)
    cap.set(3, 1280)
    cap.set(4, 720)
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    emociones_detectadas = []

    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        emocion = "Desconocido"
        if results.multi_face_landmarks:
            for rostro in results.multi_face_landmarks:
                alto, ancho, _ = frame.shape
                lista = [(int(p.x*ancho), int(p.y*alto)) for p in rostro.landmark]
                if len(lista) == 468:
                    x1, y1 = lista[65]
                    x2, y2 = lista[158]
                    l1 = math.hypot(x2-x1, y2-y1)
                    x3, y3 = lista[295]
                    x4, y4 = lista[385]
                    l2 = math.hypot(x4-x3, y4-y3)
                    x5, y5 = lista[78]
                    x6, y6 = lista[308]
                    l3 = math.hypot(x6-x5, y6-y5)
                    x7, y7 = lista[13]
                    x8, y8 = lista[14]
                    l4 = math.hypot(x8-x7, y8-y7)
                    emocion = detectar_emocion_por_longitudes(l1, l2, l3, l4)
        emociones_detectadas.append(emocion)
        if mostrar:
            cv2.putText(frame, f'Emocion: {emocion}', (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.imshow('Reconocimiento de emociones', frame)
            # Espera para capturar ~10 frames en unos 3 segundos
            if cv2.waitKey(250) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
    emociones_filtradas = [e for e in emociones_detectadas if e != "Desconocido"]
    if emociones_filtradas:
        contador = Counter(emociones_filtradas)
        emocion_predominante, cantidad = contador.most_common(1)[0]
        return emocion_predominante, cantidad, emociones_filtradas
    else:
        return "Desconocido", 0, []

def emociones_main():
    emocion_predominante, cantidad, lista = detectar_emocion_predominante()
    print(f"Emocion predominante: {emocion_predominante} ({cantidad}/10)")
    return emocion_predominante, cantidad, lista

if __name__ == "__main__":
    emocion, cantidad, lista = emociones_main()
    print(f"Emocion predominante: {emocion} ({cantidad}/10)")