
import requests
import os
from datetime import datetime

BOT_TOKEN = os.environ.get("8670280483:AAHfvP4F49GyVh9iJGLhsyke5eju-cRRbmI")
CHANNEL_ID = os.environ.get("@CryptoBrew")

def get_price():
    try:
        # نمونه API قیمت (قابل تغییر)
        data = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"
        ).json()

        btc = data["bitcoin"]["usd"]
        eth = data["ethereum"]["usd"]
        sol = data["solana"]["usd"]

        return btc, eth, sol

    except Exception:
        return "نامشخص", "نامشخص", "نامشخص"


def send_message(text):
    url = f"https://api.telegram.org/bot{8670280483:AAHfvP4F49GyVh9iJGLhsyke5eju-cRRbmI}/sendMessage"

    requests.post(url, json={
        "@CryptoBrew": CHANNEL_ID,
        "text": text
    })


btc, eth, sol = get_price()

message = f"""
💰 قیمت لحظه‌ای بازار

🔶 بیت‌کوین (BTC): {btc} $
🔷 اتریوم (ETH): {eth} $
🔸 سولانا (SOL): {sol} $

⏰ زمان بروزرسانی:
{datetime.now().strftime("%Y-%m-%d %H:%M")}
"""

send_message(message)

print("Message sent successfully")
