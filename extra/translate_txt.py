from googletrans import Translator
import time

translator = Translator()

input_file = 'extra/dialogs.txt'
output_file = 'extra/dialogs_es.txt'
batch_size = 20  # traduce 20 líneas a la vez

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

translated_lines = []
total = len(lines)
for i in range(0, total, batch_size):
    batch = lines[i:i+batch_size]
    text_to_translate = "\n".join(batch)
    try:
        translated = translator.translate(text_to_translate, src='en', dest='es')
        translated_text = translated.text.split('\n')
        # Si el número de líneas no coincide, usa traducción línea a línea como fallback
        if len(translated_text) != len(batch):
            translated_text = []
            for line in batch:
                try:
                    single = translator.translate(line, src='en', dest='es')
                    translated_text.append(single.text)
                    time.sleep(1)
                except Exception as e:
                    translated_text.append(line.strip())
        translated_lines.extend(translated_text)
        print(f"Traducidas líneas {i+1} a {min(i+batch_size, total)}")
    except Exception as e:
        print(f"Error en líneas {i+1}-{i+batch_size}: {e}")
        # Si falla, traduce línea por línea con delay
        for line in batch:
            try:
                single = translator.translate(line, src='en', dest='es')
                translated_lines.append(single.text)
                print(f"Traducida línea {i+1}: {line.strip()} -> {single.text}")
                time.sleep(1)
            except Exception as e:
                translated_lines.append(line.strip())
                print(f"Fallo traduciendo línea {i+1}: {line.strip()}")

    time.sleep(2)  # espera entre lotes, importante

# Guarda el resultado
with open(output_file, 'w', encoding='utf-8') as f:
    for line in translated_lines:
        f.write(line + '\n')

print(f"\nTraducción terminada. Archivo guardado como {output_file}")