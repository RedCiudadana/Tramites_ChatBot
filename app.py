import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Leer el archivo JSON y almacenar la información en una lista
with open("tramites.json", "r") as file:
    tramites = json.load(file)

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "ayuda" in incoming_msg:
        msg.body("¡Hola! Soy el chatbot de trámites. Puedo ayudarte a encontrar información sobre trámites disponibles. "
                 "Escribe el nombre del trámite que deseas consultar.")
    else:
        # Buscar el trámite en la lista de tramites
        found_tramite = None
        for tramite in tramites:
            if incoming_msg == tramite["name"].lower():
                found_tramite = tramite
                break

        if found_tramite:
            # Si se encontró el trámite, se envía su información
            msg.body(f"Trámite: {found_tramite['name']}\n"
                     f"Institución: {found_tramite['institution']['name']}\n"
                     f"Descripción: {found_tramite['description']}\n"
                     f"Requisitos: {found_tramite['requirements']}\n"
                     f"Costo: {found_tramite['cost']} {found_tramite['currency']['code']}\n"
                     f"Tiempo de respuesta: {found_tramite['timeResponse']}\n"
                     f"Más información: {found_tramite['url']}")
        else:
            # Si no se encontró el trámite, se envía un mensaje de error
            msg.body("Lo siento, no encontré información sobre ese trámite. Prueba escribiendo 'ayuda' para recibir asistencia.")

    return str(resp)

if __name__ == "__main__":
    app.run()
