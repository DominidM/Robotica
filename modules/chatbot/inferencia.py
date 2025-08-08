from modules.chatbot.core import (
    predict_class,
    get_response,
    retrieval_response,
)
from modules.test_psico.test_zung import (
    cargar_preguntas,
    respuesta_a_valor,
    interpretar_zung,
    guardar_resultado,
    cargar_usuario,
    ultimo_resultado_usuario,
)

def iniciar_chatbot_texto():
    print("Dimsor Chatbot iniciado! (escribe 'salir' para terminar)")
    doing_zung = False
    zung_index = 0
    zung_answers = []
    usuario = None

    while True:
        if doing_zung:
            preguntas = cargar_preguntas()
            if zung_index == 0:
                usuario = cargar_usuario()
                print(f"Usuario detectado: {usuario}")
                print("Responde cada pregunta con: muy pocas veces, algunas veces, muchas veces o casi siempre.")
            if zung_index < len(preguntas):
                print(f"Pregunta {zung_index+1}: {preguntas[zung_index]}")
                answer = input("Tu respuesta: ")
                if answer.lower() in ["salir", "terminar"]:
                    print("Saliendo de la prueba.")
                    doing_zung = False
                    zung_index = 0
                    zung_answers = []
                    usuario = None
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
                guardar_resultado(usuario if usuario else "consola", zung_answers, nivel)
                doing_zung = False
                zung_index = 0
                zung_answers = []
                usuario = None
        else:
            message = input("Tú: ")
            if message.lower() == "salir":
                print("Hasta luego.")
                break
            # Comando para consultar último resultado
            if message.lower() in ["mi resultado anterior", "último resultado", "historial"]:
                res, fecha = ultimo_resultado_usuario()
                if res:
                    print(f"Dimsor: Tu último resultado fue '{res}' el {fecha}.")
                else:
                    print("Dimsor: No tienes resultados guardados todavía.")
                continue
            ints = predict_class(message)
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

# Permite ejecución directa o desde main
if __name__ == "__main__":
    iniciar_chatbot_texto()