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


# ارزهای دیجیتال از CoinGecko
def get_crypto():

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum,solana,ripple,cardano,"
        "tron,tether&vs_currencies=usd"
    )

    headers = {
        "x-cg-demo-api-key": COINGECKO_API_KEY
    }

    data = requests.get(url, headers=headers).json()

    return {
        "BTC": data["bitcoin"]["usd"],
        "ETH": data["ethereum"]["usd"],
        "SOL": data["solana"]["usd"],
        "XRP": data["ripple"]["usd"],
        "ADA": data["cardano"]["usd"],
        "TRX": data["tron"]["usd"],
        "USDT": data["tether"]["usd"]
    }


# ارزهای جهانی
def get_currency():

    url = "https://api.exchangerate.host/latest?base=USD"

    data = requests.get(url).json()

    return data["rates"]


def create_message():

    crypto = get_crypto()
    rates = get_currency()

    # این قسمت بعداً به API قیمت واقعی ایران وصل می‌شود
    usd_toman = 420000

    gold18 = 0
    gold24 = 0
    ounce = 0
    coin = 0

    now = jdatetime.datetime.now()

    message = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا:
{format_price(usd_toman, "تومان")}

💶 یورو اروپا:
{format_price(usd_toman / rates["EUR"], "تومان")}

💷 پوند انگلیس:
{format_price(usd_toman / rates["GBP"], "تومان")}

🇨🇳 یوان چین:
{format_price(usd_toman / rates["CNY"], "تومان")}

🇦🇪 درهم امارات:
{format_price(usd_toman / rates["AED"], "تومان")}

🇸🇦 ریال عربستان:
{format_price(usd_toman / rates["SAR"], "تومان")}


🥇 اونس جهانی طلا:
{format_price(ounce, "تومان")}

🥇 طلای ۱۸ عیار:
{format_price(gold18, "تومان")}

🥇 طلای ۲۴ عیار:
{format_price(gold24, "تومان")}

🪙 سکه:
{format_price(coin, "تومان")}


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

    return message


if __name__ == "__main__":
    bot.send_message(
        chat_id=CHANNEL_ID,
        text=create_message()
    )
