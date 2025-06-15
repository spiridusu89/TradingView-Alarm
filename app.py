from flask import Flask, request
import requests
import threading
import time

app = Flask(__name__)

# Token și chat_id direct în cod
TELEGRAM_TOKEN = '7397092840:AAE99Uu7YuB5ocqLmGfy2Py9sG6kTGYR42k'
TELEGRAM_CHAT_ID = '1056585959'

# Webhook primit de la TradingView
@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    print("🔔 Primit de la TradingView:", data)

    message = data.get('message', '⚠️ Nu am primit mesaj.')

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(telegram_url, data=payload)
        print("📬 Răspuns de la Telegram:", response.status_code, response.text)

        if response.status_code == 200:
            return '✅ Trimite ok în Telegram.', 200
        else:
            return f'❌ Telegram a refuzat: {response.text}', 500

    except Exception as e:
        print("❌ Eroare gravă:", str(e))
        return f'❌ Eroare internă: {str(e)}', 500

# Endpoint GET pentru autopinging
@app.route('/', methods=['GET'])
def keepalive():
    return '✅ Online', 200

# Funcție care face ping către propriul endpoint
def autoping():
    while True:
        try:
            url = 'https://tradingview-alarm.onrender.com'
            response = requests.get(url)
            print(f"🔄 Self-ping: {response.status_code}")
        except Exception as e:
            print("⚠️ Eroare la self-ping:", e)
        time.sleep(10)

if __name__ == '__main__':
    threading.Thread(target=autoping, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
