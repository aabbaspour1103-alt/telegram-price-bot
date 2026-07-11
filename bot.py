import os
import requests

TOKEN = os.getenv("8670280483:AAHfvP4F49GyVh9iJGLhsyke5eju-cRRbmI")
CHANNEL = "@CryptoBrew"

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
