from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    print("🔔 Primit de la TradingView:", data)  # log în consolă Render

    message = data.get('message', '⚠️ No message found.')

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ TOKEN sau CHAT_ID lipsă.")
        return '❌ TOKEN sau CHAT_ID lipsă.', 500

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(telegram_url, data=payload)
    print("📬 Răspuns de la Telegram:", response.text)

    if response.status_code == 200:
        return '✅ Trimis în Telegram.', 200
    else:
        return f'❌ Eroare Telegram: {response.text}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
