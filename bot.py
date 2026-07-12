import os
import requests
import pytz
from datetime import datetime
from telegram import Bot
from khayyam import JalaliDatetime

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@CryptoBrew")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

bot = Bot(token=TOKEN)


def format_number(num):
    try:
        return f"{int(num):,}"
    except:
        return "نامشخص"


def get_time():
    tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tz)
    return JalaliDatetime(now).strftime("%Y/%m/%d - %H:%M")


# ---------- Bonbast ----------
def get_bonbast():

    url = "https://bonbast.com/api"

    headers = {}

    if os.getenv("BONBAST_API_KEY"):
        headers["Authorization"] = os.getenv("BONBAST_API_KEY")

    try:
        data = requests.get(url, headers=headers).json()

        return {
            "usd": data.get("usd"),
            "eur": data.get("eur"),
            "gbp": data.get("gbp"),
            "cny": data.get("cny"),
            "aed": data.get("aed"),
            "sar": data.get("sar"),
            "gold18": data.get("gold18"),
            "gold24": data.get("gold24"),
            "coin": data.get("coin"),
            "ounce": data.get("ounce")
        }

    except:
        return {}


# ---------- CoinGecko ----------
def get_crypto():

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids":
        "bitcoin,ethereum,solana,ripple,cardano,tron,tether",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    headers = {
        "x-cg-demo-api-key": COINGECKO_API_KEY
    }

    try:
        return requests.get(
            url,
            params=params,
            headers=headers
        ).json()

    except:
        return {}


def crypto_line(name, symbol, data):

    try:
        price = data[name]["usd"]
        change = data[name]["usd_24h_change"]

        return (
            f"{symbol} {name.upper()} ({symbol}): "
            f"${format_number(price)} "
            f"({change:.2f}%)"
        )

    except:
        return f"{symbol} {name.upper()}: نامشخص"



def main():

    bon = get_bonbast()
    cg = get_crypto()


    text = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {format_number(bon.get('usd'))} تومان
💶 یورو اروپا: {format_number(bon.get('eur'))} تومان
💷 پوند انگلیس: {format_number(bon.get('gbp'))} تومان
🇨🇳 یوان چین: {format_number(bon.get('cny'))} تومان
🇦🇪 درهم امارات: {format_number(bon.get('aed'))} تومان
🇸🇦 ریال عربستان: {format_number(bon.get('sar'))} تومان

🥇 اونس جهانی طلا: {format_number(bon.get('ounce'))} تومان
🥇 طلای ۱۸ عیار: {format_number(bon.get('gold18'))} تومان
🥇 طلای ۲۴ عیار: {format_number(bon.get('gold24'))} تومان
🪙 سکه: {format_number(bon.get('coin'))} تومان

🔶 بیت‌کوین (BTC):
{crypto_line('bitcoin','🔶',cg)}

🔷 اتریوم (ETH):
{crypto_line('ethereum','🔷',cg)}

🔸 سولانا (SOL):
{crypto_line('solana','🔸',cg)}

🔹 ریپل (XRP):
{crypto_line('ripple','🔹',cg)}

🔸 کاردانو (ADA):
{crypto_line('cardano','🔸',cg)}

🔹 ترون (TRX):
{crypto_line('tron','🔹',cg)}

💵 تتر (USDT):
{crypto_line('tether','💵',cg)}

⏰ زمان بروزرسانی:
{get_time()}

➖➖➖➖➖➖➖
@CryptoBrew
"""

    bot.send_message(
        chat_id=CHANNEL_ID,
        text=text
    )


if __name__ == "__main__":
    main()
