from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = '7860900046:AAGDUB2rZrs4lmmxy2c-2dvgYIyy2-gJoLY'
TELEGRAM_CHAT_ID = '@Market_intel_assistant_bot'

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    message = data.get('message', '⚠️ No message received.')

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(telegram_url, data=payload)

    return '✅ Message sent to Telegram', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
