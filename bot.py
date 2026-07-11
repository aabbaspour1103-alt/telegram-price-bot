import os
import requests
from datetime import datetime

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"

API_KEY = "کلید_API_شما"

url = f"https://api.navasan.tech/latest/?api_key={API_KEY}"
data = requests.get(url, timeout=20).json()

msg = f"""
📊 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {data['usd_sell']['value']} تومان
💶 یورو: {data['eur']['value']} تومان
💷 پوند انگلیس: {data['gbp']['value']} تومان
💴 درهم امارات: {data['aed']['value']} تومان
🇹🇷 لیر ترکیه: {data['try']['value']} تومان
🇨🇦 دلار کانادا: {data['cad']['value']} تومان

💰 تتر: {data['usdt']['value']} تومان
₿ بیت‌کوین: {data['btc']['value']} تومان
⟠ اتریوم: {data['eth']['value']} تومان

🥇 طلای ۱۸ عیار: {data['geram18']['value']} تومان
🥇 طلای ۲۴ عیار: {data['geram24']['value']} تومان
🌍 انس جهانی طلا: {data['ons']['value']} دلار

🪙 سکه امامی: {data['sekeb']['value']} تومان
🪙 نیم سکه: {data['nim']['value']} تومان
🪙 ربع سکه: {data['rob']['value']} تومان
🪙 سکه گرمی: {data['gerami']['value']} تومان

🕒 بروزرسانی:
{datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={"chat_id": CHANNEL_ID, "text": msg}
)
