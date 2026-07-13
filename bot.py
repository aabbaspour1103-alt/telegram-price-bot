import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from datetime import datetime
import pytz
import jdatetime


TOKEN = os.getenv("TOKEN")
CHANNEL = "@CryptoBrew"


def format_number(value):
    try:
        value = float(value)

        if value >= 1000:
            return f"{int(value):,}"

        return f"{value:,.8f}".rstrip("0").rstrip(".")
    except:
        return "نامشخص"


# دریافت قیمت دلار و ارز از TGJU
def get_tgju():

    result = {
        "usd": "نامشخص",
        "eur": "نامشخص",
        "gbp": "نامشخص",
        "aed": "نامشخص",
        "sar": "نامشخص",
        "cny": "نامشخص",
        "gold18": "نامشخص",
        "gold24": "نامشخص",
        "ounce": "نامشخص"
    }

    try:
        url = "https://www.tgju.org/"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        text = soup.get_text(" ", strip=True)

        return result

    except Exception:
        return result



# دریافت ارز دیجیتال از CoinGecko
def get_crypto():

    coins = {
        "تتر": "tether",
        "بیت‌کوین": "bitcoin",
        "اتریوم": "ethereum",
        "بایننس کوین": "binancecoin",
        "سولانا": "solana",
        "ریپل": "ripple",
        "تون": "the-open-network",
        "دوج‌کوین": "dogecoin"
    }

    result = {}

    try:
        ids = ",".join(coins.values())

        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            f"?ids={ids}&vs_currencies=usd"
        )

        data = requests.get(
            url,
            timeout=20
        ).json()

        for name, cid in coins.items():
            result[name] = format_number(
                data[cid]["usd"]
            )

    except Exception:

        for name in coins:
            result[name] = "نامشخص"

    return result



def create_message():

    market = get_tgju()
    crypto = get_crypto()


    now = datetime.now(
        pytz.timezone("Asia/Tehran")
    )

    shamsi = jdatetime.datetime.fromgregorian(
        datetime=now
    )

    date = shamsi.strftime(
        "%Y/%m/%d"
    )

    time = now.strftime(
        "%H:%M"
    )


    message = f"""
💰 قیمت لحظه‌ای بازار


💵 دلار آمریکا:
{market['usd']} تومان


💶 یورو اروپا:
{market['eur']} تومان


💷 پوند انگلیس:
{market['gbp']} تومان


🇨🇳 یوان چین:
{market['cny']} تومان


🇦🇪 درهم امارات:
{market['aed']} تومان


🇸🇦 ریال عربستان:
{market['sar']} تومان


🥇 طلا:

🌎 اونس جهانی:
{market['ounce']} دلار

🥇 طلای ۱۸ عیار:
{market['gold18']} تومان

🥇 طلای ۲۴ عیار:
{market['gold24']} تومان


🪙 ارز دیجیتال:

🟢 تتر:
{crypto['تتر']} دلار

₿ بیت‌کوین:
{crypto['بیت‌کوین']} دلار

♦️ اتریوم:
{crypto['اتریوم']} دلار

🟡 بایننس کوین:
{crypto['بایننس کوین']} دلار

🟣 سولانا:
{crypto['سولانا']} دلار

💧 ریپل:
{crypto['ریپل']} دلار

🔵 تون:
{crypto['تون']} دلار

🐶 دوج‌کوین:
{crypto['دوج‌کوین']} دلار


📅 تاریخ:
{date}

⏰ ساعت:
{time}
"""

    return message



async def main():

    bot = Bot(
        token=TOKEN
    )

    await bot.send_message(
        chat_id=CHANNEL,
        text=create_message()
    )



if __name__ == "__main__":

    import asyncio

    asyncio.run(main())
