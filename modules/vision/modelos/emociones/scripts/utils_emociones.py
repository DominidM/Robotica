import pickle

def cargar_datos_emociones(filename):
    """Carga un archivo PKL de emociones."""
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def analizar_sesion_emociones(data):
    """Imprime un resumen de los datos de una sesión."""
    session = data['session_info']
    print(f"Inicio: {session['start_time']}\nFin: {session['end_time']}")
    print(f"Total frames: {session['total_frames']}")
    print(f"Resolución: {session['resolution']}")
    print(f"Emociones detectadas: {session['emotions_detected']}")