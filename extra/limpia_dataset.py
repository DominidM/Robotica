import json

input_file = "extra/dialogs_dataset.json"
output_file = "extra/dialogs_dataset_limpio.json"

with open(input_file, encoding="utf-8") as f:
    data = json.load(f)

cleaned = [
    pair for pair in data
    if isinstance(pair, dict)
    and pair.get("output")
    and pair["output"].strip()
]

print(f"Pares originales: {len(data)}")
print(f"Pares limpios: {len(cleaned)}")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print(f"Dataset limpio guardado como {output_file}")