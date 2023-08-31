from flask import Flask, request, jsonify
from tensorflow import keras
from Feature_Extractor import extract_features
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)
user_state = {}

@app.route('/predict', methods=['GET'])
def predict():
    url = request.args.get('url')
    model_path = r"C:\Users\Barathkumar\Desktop\BETA1 (API)\model.h5"
    model = keras.models.load_model(model_path)
    url_features = extract_features(url)
    prediction = model.predict([url_features])
    score = prediction[0][0] * 100
    score = round(score, 3)
    print(score)
    return {'url': url, 'score': score}


@app.route("/whatsapp", methods=["POST"])
def reply_whatsapp():
    message_body = request.form.get("Body", "")
    sender_number = request.form.get("From", "")
    state = user_state.get(sender_number, "waiting_for_url")

    if state == "waiting_for_url":
        url = message_body.strip()
        user_state[sender_number] = "processing_url"
        greeting = ["hi","hello","hey"]
        if url.lower() in greeting:
            resp = MessagingResponse()
            resp.message("Welcome to Link SpotterX")

        elif url.startswith("http"):
            server_url = "http://localhost:5000"  
            response = requests.get(f"{server_url}/predict?url={url}")
            score = response.json()['score']

            if score < 50:
                formatted_response = f"The score for {url} is *_{score}_*. This website is safe to use ✅."
            elif score > 50 and score < 70:
                formatted_response = f"The score for {url} is {score}. Please note that this website may be harmful ⚠️."
            elif score > 70:
                formatted_response = f"The score for ~{url}~ is *_{score}_*. Please note that this website is not recommended 🚫."
            resp = MessagingResponse()
            cool=resp.message(formatted_response)
        else:
            resp = MessagingResponse()
            resp.message("I can't understand. Drop the link to detect the phishing site.")
        user_state[sender_number] = "waiting_for_url"

    elif state == "processing_url":
        resp = MessagingResponse()
        resp.message("Please wait while we process your URL.")
    return str(resp)


if __name__ == '__main__':
    app.run()
