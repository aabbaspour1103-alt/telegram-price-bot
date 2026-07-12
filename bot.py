import os
import datetime
import jdatetime
import requests
from telegram import Bot
from bonbast import Bonbast


TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=TOKEN)


def toman(value):
    try:
        return f"{int(value):,} تومان"
    except:
        return "نامشخص"


def dollar(value):
    try:
        return f"${float(value):,.2f}"
    except:
        return "نامشخص"


def get_currency():

    try:
        bb = Bonbast()
        rates = bb.get_rates()

        return {
            "usd": rates.get("usd"),
            "eur": rates.get("eur"),
            "gbp": rates.get("gbp"),
            "cny": rates.get("cny"),
            "aed": rates.get("aed"),
            "sar": rates.get("sar"),
        }

    except Exception as e:
        print(e)
        return {}


def get_crypto():

    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        
        params = {
            "ids":
            "bitcoin,ethereum,solana,ripple,cardano,tron",
            "vs_currencies": "usd"
        }

        data = requests.get(url, params=params).json()

        return {
            "btc": data["bitcoin"]["usd"],
            "eth": data["ethereum"]["usd"],
            "sol": data["solana"]["usd"],
            "xrp": data["ripple"]["usd"],
            "ada": data["cardano"]["usd"],
            "trx": data["tron"]["usd"]
        }

    except:
        return {}


def shamsi_time():

    now = jdatetime.datetime.now()

    return now.strftime(
        "%Y/%m/%d - %H:%M"
    )


def create_message():

    currency = get_currency()
    crypto = get_crypto()


    text = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {toman(currency.get('usd'))}

💶 یورو اروپا: {toman(currency.get('eur'))}

💷 پوند انگلیس: {toman(currency.get('gbp'))}

🇨🇳 یوان چین: {toman(currency.get('cny'))}

🇦🇪 درهم امارات: {toman(currency.get('aed'))}

🇸🇦 ریال عربستان: {toman(currency.get('sar'))}


🥇 اونس جهانی طلا: نامشخص

🥇 طلای ۱۸ عیار: نامشخص

🥇 طلای ۲۴ عیار: نامشخص


🔶 بیت‌کوین (BTC): {dollar(crypto.get('btc'))}

🔷 اتریوم (ETH): {dollar(crypto.get('eth'))}

🔸 سولانا (SOL): {dollar(crypto.get('sol'))}

🔹 ریپل (XRP): {dollar(crypto.get('xrp'))}

🔸 کاردانو (ADA): {dollar(crypto.get('ada'))}

🔹 ترون (TRX): {dollar(crypto.get('trx'))}


⏰ زمان بروزرسانی:
{shamsi_time()}

➖➖➖➖➖➖➖
@CryptoBrew
"""

    return text


if __name__ == "__main__":

    bot.send_message(
        chat_id=CHANNEL_ID,
        text=create_message()
    )
