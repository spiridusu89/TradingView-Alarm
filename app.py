from flask import Flask
import threading
import time
import requests
from datetime import datetime
import pytz
import logging

app = Flask(__name__)

# 🔇 Dezactivează logul Flask pentru pinguri și acces default
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# URL-ul public Render (actualizează cu ce ai tu acolo!)
BOT_URL = "https://tradingview-alarm.onrender.com"

# Fusul orar NYSE (automat gestionează și ora de vară)
ny_tz = pytz.timezone("America/New_York")

# Interval de activitate: 04:00 – 16:00 NY time
ACTIVE_HOUR_START = 4   # 04:00 AM
ACTIVE_HOUR_END = 16    # 04:00 PM

def is_nyse_active():
    now = datetime.now(ny_tz)
    return ACTIVE_HOUR_START <= now.hour < ACTIVE_HOUR_END

def silent_ping_loop():
    while True:
        if is_nyse_active():
            try:
                requests.get(BOT_URL, timeout=10)
                # nu printăm nimic, ca să păstrăm logul curat
            except:
                pass  # ignoră erorile de ping
        time.sleep(14 * 60)

@app.route("/")
def index():
    return "✅ Botul este activ."

if __name__ == "__main__":
    threading.Thread(target=silent_ping_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
