import os
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = "@YOUR_CHANNEL_ID"

message = """
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا:
💶 یورو اروپا:
💷 پوند انگلیس:
🇨🇳 یوان چین:
🇦🇪 درهم امارات:
🇹🇷 لیر ترکیه:

🥇 اونس جهانی طلا:
🥇 طلای ۱۸ عیار:
🥇 طلای ۲۴ عیار:

₿ بیت‌کوین:
🔷 اتریوم:
◎ سولانا:
✖️ ریپل:
"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHANNEL,
        "text": message
    }
)

print(response.text)
