from flask import Flask, request, jsonify
import json
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Leer el archivo JSON y almacenar la información en una lista
with open("servicios.json", "r", encoding="utf-8") as file:
    tramites_data  = json.load(file)

# Configuración de Twilio
account_sid = 'AC1383f7ef6ea036e7d6007dcd24f048b9'  # Reemplaza con tu SID de cuenta de Twilio
auth_token = '4fc22d2db296c85217144ddd23de91c8'    # Reemplaza con tu token de autenticación de Twilio
twilio_phone_number = 'whatsapp:+14155238886'  # Reemplaza con el número de teléfono de Twilio que recibirá y enviará mensajes de WhatsApp
client = Client(account_sid, auth_token)

def send_message(message):
    # Enviar el mensaje de respuesta al número de teléfono del usuario
    response = MessagingResponse()
    response.message(message)
    client.messages.create(body=response, from_=twilio_phone_number, to='whatsapp:+50258156003')  # Reemplaza 'NUMERO_DEL_USUARIO' con el número de teléfono del usuario que envió el mensaje original

# Obtener los nombres de los trámites para el cálculo de la similitud del coseno
tramite_names = [tramite['name'].lower() for tramite in tramites_data]

# Crear un vectorizador TF-IDF para calcular la similitud del coseno
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(tramite_names)

def process_message(message):
    # Convertir el mensaje del usuario a minúsculas para hacer la búsqueda insensible a mayúsculas y minúsculas
    message = message.lower()

    # Calcular el vector TF-IDF del mensaje del usuario
    message_vector = vectorizer.transform([message])

    # Calcular la similitud del coseno entre el vector del mensaje del usuario y los vectores de los nombres de los trámites
    similarity_scores = cosine_similarity(message_vector, tfidf_matrix)

    # Obtener el índice del trámite más similar (mayor similitud del coseno)
    most_similar_index = similarity_scores.argmax()

    # Obtener algunos atributos relevantes del trámite más similar
    tramite = tramites_data[most_similar_index]
    tramite_name = tramite['name']
    tramite_description = tramite['description']
    tramite_cost = tramite['cost']
    tramite_time_response = tramite['timeResponse']

    response = f"Encontré información sobre el trámite '{tramite_name}':\n"
    response += f"Descripción: {tramite_description}\n"
    response += f"Costo: {tramite_cost} {tramite['currency']['symbol']}\n"
    response += f"Tiempo de respuesta: {tramite_time_response}"

    return response

# Ruta para recibir mensajes de WhatsApp
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.form.get('Body', '').strip()
    response_message = process_message(data)  # Procesar el mensaje
    send_message(response_message)  # Enviar respuesta al usuario
    return '', 200



if __name__ == '__main__':
    app.run(debug=True)
