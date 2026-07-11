import os
import requests

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "-1003901224506"

print("TOKEN:", TOKEN)

def send_message():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    data = {
        "chat_id": CHANNEL_ID,
        "text": "✅ تست ربات انجام شد\nکانال با شناسه عددی بررسی شد."
    }

    response = requests.post(url, data=data)
    print(response.text)

send_message()
