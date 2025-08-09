import os

# Archivos .json que usa el robot y los resultados
json_files = [
    "config/usuario_sesion.json",
    "config/robot_info.json",
    "modules/test_psico/resultados.json"
]

for file in json_files:
    try:
        if os.path.exists(file):
            os.remove(file)
            print(f"✅ Archivo eliminado: {file}")
        else:
            print(f"ℹ️ El archivo no existe: {file}")
    except Exception as e:
        print(f"❌ Error al eliminar {file}: {e}")

print("Listo. Puedes iniciar el robot y las pruebas con usuario nuevo y sin historial de resultados.")