import json

input_file = "extra/dialogs_dataset.json"

with open(input_file, encoding="utf-8") as f:
    data = json.load(f)

total = len(data)
dicts = [x for x in data if isinstance(x, dict)]
dicts_with_output = [x for x in dicts if x.get("output")]
dicts_with_output_nonempty = [x for x in dicts_with_output if x["output"].strip()]
strings = [x for x in data if isinstance(x, str)]
lists = [x for x in data if isinstance(x, list)]

print(f"Total elementos: {total}")
print(f"Diccionarios: {len(dicts)}")
print(f"Diccionarios con output: {len(dicts_with_output)}")
print(f"Diccionarios con output no vacío: {len(dicts_with_output_nonempty)}")
print(f"Strings: {len(strings)}")
print(f"Listas: {len(lists)}")
print(f"Otros tipos: {total - len(dicts) - len(strings) - len(lists)}")