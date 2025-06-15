from flask import Flask, request
import requests
import threading
import time
import logging
from datetime import datetime
import pytz

# 🔕 Dezactivează logurile verbose ale serverului Flask (werkzeug)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Token și chat_id
TELEGRAM_TOKEN = '7397092840:AAE99Uu7YuB5ocqLmGfy2Py9sG6kTGYR42k'
TELEGRAM_CHAT_ID = '1056585959'

# Fus orar New York (cu suport DST)
ny_tz = pytz.timezone("America/New_York")
MARKET_OPEN_HOUR = 6    # 06:00 NY time (premarket complet)
MARKET_CLOSE_HOUR = 19  # 19:00 NY time (început after-hours)

# Verifică dacă ne aflăm în fereastra activă
def is_market_open():
    now = datetime.now(ny_tz)
    return MARKET_OPEN_HOUR <= now.hour < MARKET_CLOSE_HOUR

# Webhook primit de la TradingView (POST)
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
        print("📬 Trimis în Telegram:", response.status_code, response.text)

        if response.status_code == 200:
            return '✅ Trimis în Telegram.', 200
        else:
            return f'❌ Eroare Telegram: {response.text}', 500

    except Exception as e:
        print("❌ Eroare la trimiterea în Telegram:", str(e))
        return f'❌ Eroare internă: {str(e)}', 500

# Endpoint GET pentru ping (nu printează nimic)
@app.route('/', methods=['GET'])
def keepalive():
    return '✅ Online', 200

# Self-ping la fiecare 14 min, doar în timpul ferestrei 06–19 NY
def autoping():
    while True:
        if is_market_open():
            try:
                url = 'https://tradingview-alarm.onrender.com'
                requests.get(url, timeout=10)
            except Exception as e:
                print("⚠️ Eroare la self-ping:", e)
        time.sleep(14 * 60)

if __name__ == '__main__':
    threading.Thread(target=autoping, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
