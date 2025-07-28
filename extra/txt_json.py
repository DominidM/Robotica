import json

input_file = "extra/dialogs_es.txt"
output_file = "extra/dialogs_dataset.json"

pairs = []
with open(input_file, encoding="utf-8") as f:
    for line in f:
        # Separar por el primer punto (o usa un separador único si lo hay)
        parts = line.strip().split(".", 1)
        if len(parts) == 2:
            # Limpia espacios
            input_text = parts[0].strip() + "."
            output_text = parts[1].strip()
            pairs.append({"input": input_text, "output": output_text})

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(pairs, f, ensure_ascii=False, indent=2)

print(f"Dataset generado en {output_file}")