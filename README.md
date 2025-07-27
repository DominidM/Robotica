# Chatbot Psicológico Dimsor

Bienvenido/a al repositorio de **Dimsor**, un chatbot de apoyo emocional, conversación y orientación psicológica básica, entrenado en español. Este bot utiliza redes neuronales (Keras/TensorFlow) y procesamiento de lenguaje natural (NLTK) para entender y responder a las intenciones de los usuarios de forma más humana y cálida.

---

## Características

- Reconocimiento de intenciones (`intents.json`) enriquecido, con cientos de frases y respuestas para conversación natural.
- Soporta temas de salud emocional, conversación abierta, pruebas psicológicas básicas (como la Escala de Zung), juegos, chistes, recomendaciones musicales y más.
- Capacidad de recordar el nombre del usuario y personalizar respuestas.
- Fácil de ampliar y adaptar a nuevos temas o contextos.

---

## Instalación

### 1. Clona este repositorio

```sh
git clone https://github.com/DominidM/Robotica.git
cd Robotica
```

### 2. Crea un entorno virtual (opcional pero recomendado)

```sh
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instala las dependencias

```sh
pip install -r requirements.txt
```
O instala manualmente:

```sh
pip install tensorflow keras numpy nltk
```

---

## Archivos principales

- **chatbot.py**  
  Script principal de entrenamiento y uso del bot (modifica según tu flujo).
- **intents.json**  
  Archivo con las intenciones, patrones y respuestas del bot.
- **words.pkl / classes.pkl / chatbot_model.h5**  
  Archivos generados tras el entrenamiento.
- **README.md**  
  Este archivo.

---

## Uso

1. **Entrena el modelo**

   Ejecuta el script de entrenamiento (ajusta el nombre según tu archivo):

   ```sh
   python chatbot.py
   ```

   Esto generará los archivos `chatbot_model.h5`, `words.pkl` y `classes.pkl`.

2. **Ejecuta el bot**

   Puedes crear un script interactivo para conversar o adaptar el archivo `chatbot.py` para responder en tiempo real usando el modelo entrenado.

---

## Especificaciones técnicas

- **Python**: 3.10.0
- **Librerías**: Tensorflow, Keras, Numpy, NLTK.
- **Idioma**: Español.
- **Entrenamiento**: Basado en el archivo `intents.json`.

---

## Ejemplo de uso en consola

```sh
python chatbot.py
```
```
¡Hola! Soy Dimsor. ¿En qué puedo ayudarte hoy?
> me siento triste
Gracias por compartir cómo te sientes. Si quieres hablar más sobre eso, aquí estaré.
```

---

## Personalización

- Puedes ampliar el archivo `intents.json` con nuevos temas, patrones y respuestas.
- Si quieres que el bot use el nombre del usuario, revisa la sección “nombre del paciente” y adapta el código para guardar y reutilizar nombres.
- Agrega más intents para hacerlo más humano y realista.

---

## Créditos

Desarrollado por [SolveGrades].  
Inspirado en modelos conversacionales y datasets de uso libre.

---

## Licencia

Este proyecto es de uso educativo y experimental. Consulta el archivo LICENSE para más detalles.