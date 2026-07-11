import os
import requests

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": text
    }

    response = requests.post(url, data=data)
    print(response.text)

send_message("تست ربات")
