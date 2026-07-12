import os
import requests
from datetime import datetime
import pytz
import jdatetime
from telegram import Bot

TOKEN = os.getenv("TOKEN")
BRS_API_KEY = os.getenv("BRS_API_KEY")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

CHANNEL = "@CryptoBrew"

bot = Bot(token=TOKEN)


def format_price(value):
    try:
        return f"{int(value):,}"
    except:
        return "نامشخص"


def get_brs():

    url = f"https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency.php?key={BRS_API_KEY}"

    try:
        data = requests.get(url, timeout=10).json()

        return {
            "dollar": data.get("USD"),
            "euro": data.get("EUR"),
            "pound": data.get("GBP"),
            "yuan": data.get("CNY"),
            "aed": data.get("AED"),
            "sar": data.get("SAR"),
            "gold_ounce": data.get("ounce"),
            "gold18": data.get("gold18"),
            "gold24": data.get("gold24"),
            "coin": data.get("coin")
        }

    except:
        return {}


def get_crypto():

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids":
        "bitcoin,ethereum,solana,ripple,cardano,tron,tether",
        "vs_currencies": "usd"
    }

    headers = {
        "x-cg-demo-api-key": COINGECKO_API_KEY
    }

    try:
        r = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        return r.json()

    except:
        return {}


def create_message():

    brs = get_brs()
    crypto = get_crypto()


    tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tz)

    shamsi = jdatetime.datetime.fromgregorian(
        datetime=now
    )

    date = shamsi.strftime(
        "%Y/%m/%d %H:%M"
    )


    text = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {format_price(brs.get('dollar'))} تومان

💶 یورو اروپا: {format_price(brs.get('euro'))} تومان

💷 پوند انگلیس: {format_price(brs.get('pound'))} تومان

🇨🇳 یوان چین: {format_price(brs.get('yuan'))} تومان

🇦🇪 درهم امارات: {format_price(brs.get('aed'))} تومان

🇸🇦 ریال عربستان: {format_price(brs.get('sar'))} تومان

🥇 اونس جهانی طلا: {format_price(brs.get('gold_ounce'))} تومان

🥇 طلای ۱۸ عیار: {format_price(brs.get('gold18'))} تومان

🥇 طلای ۲۴ عیار: {format_price(brs.get('gold24'))} تومان

🪙 سکه امامی: {format_price(brs.get('coin'))} تومان


🔶 بیت‌کوین (BTC): {crypto.get('bitcoin',{}).get('usd','نامشخص'):,} دلار

🔷 اتریوم (ETH): {crypto.get('ethereum',{}).get('usd','نامشخص'):,} دلار

🔸 سولانا (SOL): {crypto.get('solana',{}).get('usd','نامشخص'):,} دلار

🔹 ریپل (XRP): {crypto.get('ripple',{}).get('usd','نامشخص'):,} دلار

🔸 کاردانو (ADA): {crypto.get('cardano',{}).get('usd','نامشخص'):,} دلار

🔹 ترون (TRX): {crypto.get('tron',{}).get('usd','نامشخص'):,} دلار

💲 تتر (USDT): {crypto.get('tether',{}).get('usd','نامشخص'):,} دلار


⏰ زمان بروزرسانی:
{date}

➖➖➖➖➖➖➖
@CryptoBrew
"""

    return text


if __name__ == "__main__":

    message = create_message()

    bot.send_message(
        chat_id=CHANNEL,
        text=message
    )
