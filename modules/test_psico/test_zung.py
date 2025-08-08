import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "test_psico")
RESULTADOS_PATH = os.path.abspath(os.path.join(DATA_DIR, "resultados.json"))
PREGUNTAS_PATH = os.path.join(DATA_DIR, "preguntas.json")

zung_reverse_questions = [2, 5, 6, 11, 12, 14, 16, 17, 18, 20]

text_to_score = {
    1: ["muy pocas veces", "nunca", "casi nunca", "nada", "jamás", "ninguna vez", "para nada", "raramente", "pocas veces"],
    2: ["algunas veces", "a veces", "ocasionalmente", "poco", "de vez en cuando"],
    3: ["muchas veces", "frecuentemente", "a menudo", "bastante", "seguido", "considerablemente"],
    4: ["casi siempre", "siempre", "todo el tiempo", "la mayoría de las veces", "muy frecuente"]
}
zung_reverse = {4:1, 3:2, 2:3, 1:4}

def cargar_usuario():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../config/usuario_sesion.json"))
    try:
        with open(config_path, encoding="utf-8") as f:
            data = json.load(f)
        usuario = data.get("nombre", "Anonimo")
        registro = data.get("registro_key", "")
        return f"{usuario} ({registro})" if registro else usuario
    except Exception:
        return "Anonimo"

def cargar_preguntas():
    with open(PREGUNTAS_PATH, encoding="utf-8") as f:
        return json.load(f)

def respuesta_a_valor(texto):
    texto = texto.strip().lower()
    for val, palabras in text_to_score.items():
        for palabra in palabras:
            if palabra in texto:
                return val
    if texto in ["1", "2", "3", "4"]:
        return int(texto)
    return None

def interpretar_zung(respuestas):
    puntaje = 0
    for idx, r in enumerate(respuestas):
        valor = r
        if (idx+1) in zung_reverse_questions:
            valor = zung_reverse.get(valor, valor)
        puntaje += valor
    if puntaje <= 28:
        nivel = "Ausencia de depresión"
    elif 29 <= puntaje <= 41:
        nivel = "Depresión leve"
    elif 42 <= puntaje <= 53:
        nivel = "Depresión moderada"
    else:
        nivel = "Depresión grave"
    return nivel

def guardar_resultado(usuario, respuestas, resultado):
    entrada = {
        "usuario": usuario,
        "fecha": datetime.now().isoformat(),
        "respuestas": respuestas,
        "resultado": resultado
    }
    datos = []
    if os.path.exists(RESULTADOS_PATH):
        try:
            with open(RESULTADOS_PATH, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if contenido and contenido != "[]":
                    datos = json.loads(contenido)
                elif contenido == "[]":
                    datos = []
        except Exception as e:
            print(f"Error leyendo resultados.json: {e}")
            datos = []
    datos.append(entrada)
    try:
        with open(RESULTADOS_PATH, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        print("Resultado guardado correctamente en resultados.json.")
    except Exception as e:
        print(f"Error guardando resultados.json: {e}")

def mostrar_historial(usuario=None):
    """Muestra todos los resultados guardados, opcionalmente filtrados por usuario"""
    if os.path.exists(RESULTADOS_PATH):
        with open(RESULTADOS_PATH, "r", encoding="utf-8") as f:
            datos = json.load(f)
            if usuario:
                datos = [d for d in datos if d.get("usuario") == usuario]
            for test in datos:
                fecha_iso = test["fecha"]
                fecha_dt = datetime.fromisoformat(fecha_iso)
                fecha_str = fecha_dt.strftime("%d/%m/%Y")
                print(f"Usuario: {test['usuario']}")
                print(f"Fecha: {fecha_str}")
                print(f"Resultado: {test['resultado']}")
                print("-" * 30)
    else:
        print("No hay historial.")

def ultimo_resultado_usuario(usuario=None):
    """
    Devuelve el último resultado guardado para el usuario indicado.
    Si usuario=None, muestra el último del usuario actual (de usuario_sesion.json).
    Retorna (resultado, fecha_str) o (None, None) si no hay datos
    """
    if usuario is None:
        usuario = cargar_usuario()
    if os.path.exists(RESULTADOS_PATH):
        with open(RESULTADOS_PATH, "r", encoding="utf-8") as f:
            datos = json.load(f)
            resultados_usuario = [test for test in datos if test.get("usuario") == usuario]
            if resultados_usuario:
                ultimo = resultados_usuario[-1]
                fecha_iso = ultimo["fecha"]
                fecha_dt = datetime.fromisoformat(fecha_iso)
                fecha_str = fecha_dt.strftime("%d/%m/%Y")
                return ultimo['resultado'], fecha_str
            else:
                return None, None
    else:
        return None, None

def administrar_test():
    preguntas = cargar_preguntas()
    respuestas = []
    usuario = cargar_usuario()
    print(f"Usuario detectado: {usuario}")
    print("Responde cada pregunta con: muy pocas veces, algunas veces, muchas veces o casi siempre.")
    for idx, pregunta in enumerate(preguntas):
        print(f"Pregunta {idx+1}: {pregunta}")
        respuesta = input("Tu respuesta: ")
        valor = respuesta_a_valor(respuesta)
        while valor is None:
            print("Respuesta no válida. Por favor responde con: muy pocas veces, algunas veces, muchas veces o casi siempre (o 1, 2, 3, 4).")
            respuesta = input("Tu respuesta: ")
            valor = respuesta_a_valor(respuesta)
        respuestas.append(valor)
    resultado = interpretar_zung(respuestas)
    print(f"\nResultado de la prueba: {resultado}")
    guardar_resultado(usuario, respuestas, resultado)

if __name__ == "__main__":
    administrar_test()