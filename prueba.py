import json

# Antes de hacer json.loads(), imprime exactamente qué tienes
print("Tipo de variable:", type(tu_variable_json))
print("Contenido repr:", repr(tu_variable_json))
print("Longitud:", len(tu_variable_json) if tu_variable_json else 0)
print("Primeros 100 caracteres:", tu_variable_json[:100] if tu_variable_json else "VACIO")

# Entonces intenta parsear
try:
    data = json.loads(tu_variable_json)
    print("✅ JSON parseado correctamente")
except Exception as e:
    print(f"❌ Error: {e}")