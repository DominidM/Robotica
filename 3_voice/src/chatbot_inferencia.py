from chatbot_core import (
    predict_class,
    get_response,
    retrieval_response,
    zung_questions,
    respuesta_a_valor,
    interpretar_zung,
)

print("Dimsor Chatbot iniciado! (escribe 'salir' para terminar)")
doing_zung = False
zung_index = 0
zung_answers = []

while True:
    if doing_zung:
        if zung_index == 0:
            print("Responde cada pregunta con: muy pocas veces, algunas veces, muchas veces o casi siempre.")
        if zung_index < len(zung_questions):
            print(f"Pregunta {zung_index+1}: {zung_questions[zung_index]}")
            answer = input("Tu respuesta: ")
            if answer.lower() in ["salir", "terminar"]:
                print("Saliendo de la prueba.")
                doing_zung = False
                zung_index = 0
                zung_answers = []
                continue
            valor = respuesta_a_valor(answer)
            if valor is not None:
                zung_answers.append(valor)
                zung_index += 1
            else:
                print("Por favor responde con: muy pocas veces, algunas veces, muchas veces o casi siempre.")
                continue
        else:
            nivel = interpretar_zung(zung_answers)
            print(f"Resultado de la prueba: {nivel}.")
            doing_zung = False
            zung_index = 0
            zung_answers = []
    else:
        message = input("Tú: ")
        if message.lower() == "salir":
            print("Hasta luego.")
            break
        ints = predict_class(message)
        # Lógica híbrida: usa retrieval si la predicción de intent es baja o no hay intent claro
        if not ints or float(ints[0]['probability']) < 0.4:
            res = retrieval_response(message)
            print("Dimsor (retrieval):", res)
        else:
            res, tag = get_response(ints)
            print("Dimsor:", res)
            if tag == "realizar prueba":
                doing_zung = True
                zung_index = 0
                zung_answers = []