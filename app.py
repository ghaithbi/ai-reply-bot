# app.py
import requests
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()
from bot_logic import qa_chain

PAGE_ACCESS_TOKEN = "EAAOpMh623y8BPDZClaLvN57q4ZBv2PvZB4u60r6srWJaRqenZCwIRvJb7yQ8vpTtpTWOFOGE5r25eS6YOOv5tpZCasPKTHQDzZALmrcwvP98BzflDRdBOpeRphPps2Lgahi2nDkZANiyI4Qf4sX2qPkmYR2MdlVkYg4IbZBRDTc8GuwfkJdOfEpGg50Udt9P4HUiIx3zEu2jdGN72CYC3CQq3KbI8AZDZD"
VERIFY_TOKEN = "saphiredent-secret-token"
PAGE_ID = "649673271573699"
GRAPH_API_URL = f"https://graph.facebook.com/v20.0/{PAGE_ID}/messages"

app = Flask(__name__)

@app.route('/')
def index(): return "<h1>SaphireDent Bot is running!</h1>"

def send_reply(sender_id, message_text):
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {"recipient": {"id": sender_id}, "message": {"text": message_text}}
    requests.post(GRAPH_API_URL, params=params, headers=headers, json=data)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == "saphiredent-secret-token": # Direct comparison for safety
            return challenge, 200
        else:
            return 'Verification token mismatch', 403

    elif request.method == 'POST':
        payload = request.get_json()
        if payload.get("object") == "page":
            for entry in payload.get("entry", []):
                for message in entry.get("messaging", []):
                    if message.get("message"):
                        sender_id = message["sender"]["id"]
                        message_text = message["message"].get("text", "").strip()

                        ai_response = qa_chain.invoke({"question": message_text})
                        reply_text = ai_response.get("answer", "Sorry, I'm having a little trouble right now.")
                        send_reply(sender_id, reply_text)
        return 'EVENT_RECEIVED', 200
    return 'Not Found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

