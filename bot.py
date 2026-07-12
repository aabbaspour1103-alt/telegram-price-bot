import os
import requests
from datetime import datetime
import jdatetime
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"

bot = Bot(token=TOKEN)


def format_price(value, unit=""):
    if value is None:
        return "نامشخص"

    if value < 1:
        return f"{value:.8f} {unit}"

    return f"{value:,.0f} {unit}"


def get_crypto():

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum,solana,ripple,"
        "cardano,tron,tether&vs_currencies=usd"
    )

    data = requests.get(url).json()

    return {
        "BTC": data["bitcoin"]["usd"],
        "ETH": data["ethereum"]["usd"],
        "SOL": data["solana"]["usd"],
        "XRP": data["ripple"]["usd"],
        "ADA": data["cardano"]["usd"],
        "TRX": data["tron"]["usd"],
        "USDT": data["tether"]["usd"]
    }


def get_currency():

    url = "https://api.exchangerate.host/latest?base=USD"

    data = requests.get(url).json()

    return data["rates"]


def get_message():

    crypto = get_crypto()
    rates = get_currency()

    usd_to_toman = 420000

    now = jdatetime.datetime.now()

    return f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {format_price(usd_to_toman)} تومان

💶 یورو اروپا: {format_price(usd_to_toman / rates['EUR'])} تومان

💷 پوند انگلیس: {format_price(usd_to_toman / rates['GBP'])} تومان

🇨🇳 یوان چین: {format_price(usd_to_toman / rates['CNY'])} تومان

🇦🇪 درهم امارات: {format_price(usd_to_toman / rates['AED'])} تومان

🇸🇦 ریال عربستان: {format_price(usd_to_toman / rates['SAR'])} تومان


🥇 اونس جهانی طلا: قیمت دلاری

🥇 طلای ۱۸ عیار: قیمت تومان

🥇 طلای ۲۴ عیار: قیمت تومان

🪙 سکه: قیمت تومان


🔶 بیت‌کوین (BTC):
{format_price(crypto['BTC'])} $

🔷 اتریوم (ETH):
{format_price(crypto['ETH'])} $

🔸 سولانا (SOL):
{format_price(crypto['SOL'])} $

🔹 ریپل (XRP):
{format_price(crypto['XRP'])} $

🔸 کاردانو (ADA):
{format_price(crypto['ADA'])} $

🔹 ترون (TRX):
{format_price(crypto['TRX'])} $

💵 تتر (USDT):
{format_price(crypto['USDT'])} $


⏰ زمان بروزرسانی:
{now.strftime("%Y/%m/%d - %H:%M")}

➖➖➖➖➖➖➖
@CryptoBrew
"""


if __name__ == "__main__":
    bot.send_message(
        chat_id=CHANNEL_ID,
        text=get_message()
    )
