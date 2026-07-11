import os
import requests

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"

print("شروع تست")
print("TOKEN:", TOKEN)

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHANNEL_ID,
    "text": "تست ربات"
}

response = requests.post(url, data=data)

print(response.text)
print("پایان تست")
