# Chatbot Psicológico Dimsor 🤖🧠

¡Bienvenido/a al repositorio de **Dimsor**!  
Dimsor es un chatbot de apoyo emocional y orientación psicológica básica, entrenado en español para brindar compañía, conversación cálida y herramientas de autoayuda. Utiliza **redes neuronales (Keras/TensorFlow)** y **procesamiento de lenguaje natural (NLTK)** para comprender y responder de forma humanizada.

---

## 🚀 Repositorios y Ecosistema

- [Robotica-Web (Interfaz Web)](https://github.com/DominidM/Robotica-Web)
- [Robotica-Mobile (Interfaz Móvil)](https://github.com/DominidM/Robotica-Mobile)

---

## ✨ Características principales

- **Reconocimiento avanzado de intenciones** (`intents.json` enriquecido) para conversación natural.
- Temas de salud emocional, conversación general, pruebas psicológicas (Ej: Escala de Zung), juegos, chistes, recomendaciones musicales y mucho más.
- **Personalización:** recuerda el nombre del usuario y adapta sus respuestas.
- Fácil de **extender y adaptar** a nuevos temas/contextos.
- Integrable con interfaces web/móvil y sistemas de robótica.

---

## ⚙️ Instalación y configuración

### 1. Clona el repositorio

```sh
git clone https://github.com/DominidM/Robotica.git
cd Robotica
```

### 2. (Opcional) Crea un entorno virtual

```sh
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
```

### 3. Instala las dependencias

```sh
pip install -r requirements.txt
```
O manualmente:
```sh
pip install tensorflow keras numpy nltk
```

---

## 📂 Estructura de archivos

- **chatbot.py**  
  Script principal para entrenar y ejecutar el bot.
- **intents.json**  
  Intenciones, patrones y respuestas del bot.
- **words.pkl / classes.pkl / chatbot_model.h5**  
  Archivos generados tras el entrenamiento.
- **modules/**  
  Funcionalidades avanzadas (voz, motores, visión, tests psicológicos, etc.)
- **README.md**  
  Este archivo.

---

## 🧑‍💻 Uso rápido

1. **Entrena el modelo**

   ```sh
   python chatbot.py
   ```
   Esto generará los archivos `chatbot_model.h5`, `words.pkl` y `classes.pkl`.

2. **Conversar con el bot**

   Ejecuta el bot (puedes adaptar el script para consola, web, móvil o robótica):

   ```sh
   python chatbot.py
   ```

   Ejemplo de interacción:
   ```
   ¡Hola! Soy Dimsor. ¿En qué puedo ayudarte hoy?
   > me siento triste
   Gracias por compartir cómo te sientes. Si quieres hablar más sobre eso, aquí estaré.
   ```

---

## 🛠️ Personalización y ampliación

- **Agrega nuevos temas y respuestas:** Edita `intents.json` para ampliar el vocabulario y los contextos del bot.
- **Recuerda el nombre del usuario:** Adapta el código para guardar y reutilizar nombres.
- **Modos avanzados:** Integra módulos de voz, visión (seguimiento por cámara), motores (robótica), tests psicológicos y más desde la carpeta `modules/`.

---

## 📝 Especificaciones técnicas

- **Python:** 3.10.0
- **Librerías:** Tensorflow, Keras, Numpy, NLTK
- **Idioma:** Español
- **Entrenamiento:** Basado en `intents.json`

---

## 🌱 Créditos

Desarrollado por [SolveGrades].  
Inspirado en modelos conversacionales y datasets de uso libre.

---

## 📜 Licencia

Este proyecto es de uso educativo y experimental.  
Consulta el archivo LICENSE para más detalles.

---