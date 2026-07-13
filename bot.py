import os
import requests
from datetime import datetime
import pytz
import jdatetime
import asyncio
from telegram import Bot


TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"
NAVASAN_API_KEY = os.getenv("NAVASAN_API_KEY")


def safe_request(url):
    try:
        response = requests.get(url, timeout=15)

        if response.status_code == 200:
            return response.json()

    except Exception:
        pass

    return {}


def format_number(value, decimals=False):
    try:
        if value is None:
            return "نامشخص"

        num = float(value)

        if not decimals:
            return f"{int(num):,}"

        if num >= 1000:
            return f"{int(num):,}"

        return f"{num:,.6f}".rstrip("0").rstrip(".")

    except:
        return "نامشخص"


def get_value(data, keys):

    try:
        for key in keys:

            if key in data:

                item = data[key]

                if isinstance(item, dict):
                    return (
                        item.get("value")
                        or item.get("price")
                        or item.get("current")
                    )

                return item

    except:
        pass

    return None



def get_navasan():

    result = {}

    try:

        url = (
            "https://api.navasan.tech/latest/"
            f"?api_key={NAVASAN_API_KEY}"
        )

        data = safe_request(url)

        result = {

            "usd": get_value(data, ["usd","usd_sell","dollar"]),
            "eur": get_value(data, ["eur","euro"]),
            "gbp": get_value(data, ["gbp","pound"]),
            "cny": get_value(data, ["cny","yuan"]),
            "aed": get_value(data, ["aed","dirham"]),
            "sar": get_value(data, ["sar"]),
            "try": get_value(data, ["try"]),
            "rub": get_value(data, ["rub"]),
            "cad": get_value(data, ["cad"]),
            "aud": get_value(data, ["aud"])

        }


    except:
        pass


    return result



def get_crypto():

    coins = {

        "BTC":"bitcoin",
        "ETH":"ethereum",
        "BNB":"binancecoin",
        "SOL":"solana",
        "XRP":"ripple",
        "TON":"the-open-network",
        "DOGE":"dogecoin",
        "ADA":"cardano",
        "AVAX":"avalanche-2",
        "DOT":"polkadot",
        "LTC":"litecoin",
        "SHIB":"shiba-inu"

    }


    result = {}


    try:

        ids = ",".join(coins.values())

        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            f"?ids={ids}&vs_currencies=usd"
        )


        data = safe_request(url)


        for name, key in coins.items():

            try:
                result[name] = data[key]["usd"]

            except:
                result[name] = None


    except:
        pass


    return result



def iran_time():

    try:

        tz = pytz.timezone("Asia/Tehran")

        now = datetime.now(tz)

        jalali = jdatetime.datetime.fromgregorian(
            datetime=now
        )

        return jalali.strftime("%Y/%m/%d - %H:%M")

    except:

        return "نامشخص"



def create_message():

    money = get_navasan()

    crypto = get_crypto()


    return f"""
💰 قیـمت لحظه‌ای بازار

🥈 ارز :

💵 دلار آمریکـــــــا: {format_number(money.get('usd'))} تومان
💶 یــــورو اروپـــا: {format_number(money.get('eur'))} تومان
💷 پـــوند انگلیس: {format_number(money.get('gbp'))} تومان
🇨🇳 یــــوان چـــین: {format_number(money.get('cny'))} تومان
🇦🇪 درهــم امارات: {format_number(money.get('aed'))} تومان
🇸🇦 ریال عربستان: {format_number(money.get('sar'))} تومان
🇹🇷 لـــــیــــر ترکیه: {format_number(money.get('try'))} تومان
🇷🇺 روبـــل روسیه: {format_number(money.get('rub'))} تومان
🇨🇦 دلار کـــــــانادا: {format_number(money.get('cad'))} تومان
🇦🇺 دلار اســترالیا: {format_number(money.get('aud'))} تومان


🥇 ارز دیجیتال:

🔶 بیــــت‌کوین (BTC): {format_number(crypto.get('BTC'),True)} دلار
🔷 اتــــریــــــوم (ETH): {format_number(crypto.get('ETH'),True)} دلار
🔸 بایننس‌کوین (BNB): {format_number(crypto.get('BNB'),True)} دلار
🔹 ســــــــــولانا (SOL): {format_number(crypto.get('SOL'),True)} دلار
🔸 ریـــــــــــــپل (XRP): {format_number(crypto.get('XRP'),True)} دلار
🔹 تـــــون‌کوین (TON): {format_number(crypto.get('TON'),True)} دلار
🔸 دوج‌کـوین (DOGE): {format_number(crypto.get('DOGE'),True)} دلار
🔹 کـــاردانــــــو (ADA): {format_number(crypto.get('ADA'),True)} دلار
🔸 آوالانـــــــچ (AVAX): {format_number(crypto.get('AVAX'),True)} دلار
🔹 پولـــکـــادات (DOT): {format_number(crypto.get('DOT'),True)} دلار
🔸 لایــــــت‌کوین (LTC): {format_number(crypto.get('LTC'),True)} دلار
🔹 شیـــــبا اینو (SHIB): {format_number(crypto.get('SHIB'),True)} دلار


🕒 بــروزرسانــی: {iran_time()}

- @CryptoBrew
"""



async def main():

    try:

        bot = Bot(token=TOKEN)

        message = create_message()

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=message
        )

    except Exception as e:

        print("Telegram Error:", e)



if __name__ == "__main__":

    asyncio.run(main())
