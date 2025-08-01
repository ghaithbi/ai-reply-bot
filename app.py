# app.py
import requests
import re
import os
import smtplib, ssl
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()
from bot_logic import qa_chain

# --- Configuration ---
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = "saphiredent-secret-token"
PAGE_ID = "649673271573699"
GRAPH_API_URL = f"https://graph.facebook.com/v20.0/{PAGE_ID}/messages"

# --- Email Configuration ---
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

app = Flask(__name__)

@app.route('/')
def index(): return "<h1>SaphireDent Bot is running!</h1>"

def send_reply(sender_id, message_text):
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {"recipient": {"id": sender_id}, "message": {"text": message_text}}
    requests.post(GRAPH_API_URL, params=params, headers=headers, json=data)

def send_email_report(contact_message):
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        print("Email credentials not set. Skipping email report.")
        return

    subject = "New Lead from Meta Chatbot (Manual Entry)"
    body = f"A new potential client has provided their contact information directly in the chat:\n\n---\n{contact_message}\n---"
    message = f"Subject: {subject}\n\n{body}"

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.encode('utf-8'))
            print("Successfully sent email report.")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # ... (GET request logic remains the same)
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN:
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

                        # --- New Advanced Contact Info Detection Logic ---

                        # Check for the specific keywords of a form submission
                        contains_contact_keywords = "full_name:" in message_text.lower() and "email:" in message_text.lower() and "phone_number:" in message_text.lower()

                        # Check for the exclusionary phrase
                        is_from_form = "filled in your form" in message_text.lower()

                        instruction = ""
                        if contains_contact_keywords and not is_from_form:
                            # If it looks like contact info AND is NOT from the form, send an email.
                            send_email_report(message_text)
                            instruction = "The user has provided their contact info. Thank them and confirm a consultant will be in touch."

                        final_question = f"INTERNAL INSTRUCTION: {instruction}\n\nUSER MESSAGE: {message_text}"

                        ai_response = qa_chain.invoke({"question": final_question})
                        reply_text = ai_response.get("answer", "Sorry, I'm having a little trouble right now.")
                        send_reply(sender_id, reply_text)
        return 'EVENT_RECEIVED', 200
    return 'Not Found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

