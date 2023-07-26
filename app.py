from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

# Leer el archivo JSON y almacenar la información en una lista
with open("servicios.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    
@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower().strip()
    resp = MessagingResponse()
    msg = resp.message()
    response_message = ""

    # Lógica del chatbot
    if 'consulta' in incoming_msg:
        response_message = "¡Bienvenido al chatbot de consultas! Por favor, ingresa el nombre del trámite que deseas consultar."
    else:
        # Buscar el trámite en el archivo JSON
        result = next((servicio for servicio in data if servicio['name'].lower() == incoming_msg), None)
        if result:
            response_message = f"Nombre: {result['name']}\n"
            response_message += f"Descripción: {result['description']}\n"
            response_message += f"Institución: {result['institution']['name']}\n"
            response_message += f"Categoría: {result['subcategory']['name']}\n"
            response_message += f"Costo: {result['cost']} {result['currency']['symbol']}\n"
            response_message += f"Tiempo de Respuesta: {result['timeResponse']}\n"
            response_message += f"Normativa: {result['normative']}\n"
            response_message += f"Más información: {result['url']}"
        else:
            response_message = "Lo siento, no encontré información sobre ese trámite. Por favor, intenta con otro nombre."

    msg.body(response_message)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)