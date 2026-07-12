import os
import requests
import jdatetime
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

bot = Bot(token=TOKEN)


def format_price(value, unit):
    if value is None:
        return "نامشخص"

    if abs(value) < 1:
        return f"{value:.8f} {unit}"

    return f"{value:,.0f} {unit}"


# ارزهای دیجیتال
def get_crypto():

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum,solana,ripple,cardano,"
        "tron,tether&vs_currencies=usd"
    )

    headers = {
        "x-cg-demo-api-key": COINGECKO_API_KEY
    }

    response = requests.get(url, headers=headers, timeout=15)
    data = response.json()

    return {
        "BTC": data.get("bitcoin", {}).get("usd", 0),
        "ETH": data.get("ethereum", {}).get("usd", 0),
        "SOL": data.get("solana", {}).get("usd", 0),
        "XRP": data.get("ripple", {}).get("usd", 0),
        "ADA": data.get("cardano", {}).get("usd", 0),
        "TRX": data.get("tron", {}).get("usd", 0),
        "USDT": data.get("tether", {}).get("usd", 0)
    }


# ارزهای جهانی
def get_currency():

    url = "https://api.exchangerate.host/latest?base=USD"

    try:
        response = requests.get(url, timeout=15)
        data = response.json()

        if "rates" in data:
            return data["rates"]

    except Exception:
        pass

    return {
        "EUR": 0,
        "GBP": 0,
        "CNY": 0,
        "AED": 0,
        "SAR": 0
    }


def create_message():

    crypto = get_crypto()
    rates = get_currency()

    # فعلاً مقدار پایه - بعداً با API ایران جایگزین می‌شود
    usd_toman = 420000

    now = jdatetime.datetime.now()

    return f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا:
{format_price(usd_toman, "تومان")}

💶 یورو اروپا:
{format_price(usd_toman / rates["EUR"] if rates["EUR"] else 0, "تومان")}

💷 پوند انگلیس:
{format_price(usd_toman / rates["GBP"] if rates["GBP"] else 0, "تومان")}

🇨🇳 یوان چین:
{format_price(usd_toman / rates["CNY"] if rates["CNY"] else 0, "تومان")}

🇦🇪 درهم امارات:
{format_price(usd_toman / rates["AED"] if rates["AED"] else 0, "تومان")}

🇸🇦 ریال عربستان:
{format_price(usd_toman / rates["SAR"] if rates["SAR"] else 0, "تومان")}


🥇 اونس جهانی طلا:
نامشخص تومان

🥇 طلای ۱۸ عیار:
نامشخص تومان

🥇 طلای ۲۴ عیار:
نامشخص تومان

🪙 سکه:
نامشخص تومان


🔶 بیت‌کوین (BTC):
{format_price(crypto["BTC"], "$")}

🔷 اتریوم (ETH):
{format_price(crypto["ETH"], "$")}

🔸 سولانا (SOL):
{format_price(crypto["SOL"], "$")}

🔹 ریپل (XRP):
{format_price(crypto["XRP"], "$")}

🔸 کاردانو (ADA):
{format_price(crypto["ADA"], "$")}

🔹 ترون (TRX):
{format_price(crypto["TRX"], "$")}

💵 تتر (USDT):
{format_price(crypto["USDT"], "$")}


⏰ زمان بروزرسانی:
{now.strftime("%Y/%m/%d - %H:%M")}

➖➖➖➖➖➖➖
@CryptoBrew
"""


if __name__ == "__main__":
    bot.send_message(
        chat_id=CHANNEL_ID,
        text=create_message()
    )
