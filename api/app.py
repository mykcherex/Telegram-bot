import os
import requests
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# 🔑 Token credentials
TELEGRAM_TOKEN = "8833551215:AAHGfXL5dvSsUKrMP6cnxqcIFw6bfqJgCNw"
GEMINI_API_KEY = "AQ.Ab8RN6L7NsIaYIXtijHlJVT-_DVJsvH5TsFC2mpZaAwCe03GPQ"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "")
        
        # Avoid responding to slash commands like /start
        if user_text and not user_text.startswith('/'):
            try:
                response = model.generate_content(user_text)
                ai_reply = response.text
            except Exception as e:
                ai_reply = "Sorry, I encountered an error processing that with Gemini AI."
            
            # Corrected endpoint destination URL
            telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": ai_reply
            }
            requests.post(telegram_url, json=payload)
            
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
          
