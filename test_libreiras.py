import os

# Archivos y carpetas esenciales
archivos = [
    "main.py",
    "modules/vision/modelos/senas/models/abecedario_model.pkl",
    "modules/chatbot/core.py",
    "modules/chatbot/inferencia.py",
    "modules/chatbot/voz.py",
    "modules/vision/seguimiento_persona.py",
    "sound/beep.mp3",
    "sound/sonido_inicio.mp3",
    "config/robot_info.json",
    "config/usuario_sesion.json",
    "config/sesion_actual.json"
]

# Carpetas que deben tener __init__.py
carpetas_init = [
    "modules",
    "modules/chatbot",
    "modules/vision",
    "modules/vision/modelos",
    "modules/vision/modelos/senas",
    "modules/vision/modelos/senas/models",
    "modules/test_psico"
]

def verifica_archivos():
    print("Verificando archivos esenciales:")
    ok = True
    for f in archivos:
        if not os.path.exists(f):
            print(f"❌ Falta: {f}")
            ok = False
        else:
            print(f"✅ OK: {f}")
    return ok

def crea_inits():
    print("\nVerificando y creando __init__.py donde falte:")
    for folder in carpetas_init:
        path = os.path.join(folder, "__init__.py")
        if not os.path.exists(path):
            open(path, "w").close()
            print(f"🆕 Creado: {path}")
        else:
            print(f"✅ Ya existe: {path}")

if __name__ == "__main__":
    todo_ok = verifica_archivos()
    crea_inits()
    if todo_ok:
        print("\nTodo está presente. ¡Listo para ejecutar el proyecto!")
    else:
        print("\nCorrige los archivos faltantes antes de continuar.")