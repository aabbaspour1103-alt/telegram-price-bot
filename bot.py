import os
import requests
import jdatetime
from bs4 import BeautifulSoup
from telegram import Bot
from datetime import datetime


# ==========================
# Environment Variables
# ==========================

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")


bot = Bot(token=TOKEN)


# ==========================
# Helpers
# ==========================

def format_price(value):
    try:
        value = int(float(value))
        return f"{value:,} تومان"
    except:
        return "نامشخص"


def format_usd(value):
    try:
        return f"${float(value):,.2f}"
    except:
        return "نامشخص"


def get_jalali_date():
    now = jdatetime.datetime.now()
    return now.strftime("%Y/%m/%d - %H:%M")


def safe_request(url, headers=None):
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()
        return response.text

    except Exception as e:
        print("Request Error:", e)
        return None
        # ==========================
# TGJU Scraper
# ==========================

def get_tgju_prices():

    prices = {
        "usd": "نامشخص",
        "eur": "نامشخص",
        "gbp": "نامشخص",
        "cny": "نامشخص",
        "aed": "نامشخص",
        "sar": "نامشخص",
        "gold_ounce": "نامشخص",
        "gold_18": "نامشخص",
        "gold_24": "نامشخص"
    }

    try:
        url = "https://www.tgju.org/"
        
        headers = {
            "User-Agent":
            "Mozilla/5.0"
        }

        html = safe_request(url, headers)

        if not html:
            return prices

        soup = BeautifulSoup(html, "lxml")


        # جستجوی نمادها در صفحه
        items = soup.find_all(
            "tr"
        )


        for item in items:
            text = item.get_text(
                " ",
                strip=True
            )

            if "دلار" in text:
                prices["usd"] = text

            elif "یورو" in text:
                prices["eur"] = text

            elif "پوند" in text:
                prices["gbp"] = text

            elif "یوان" in text:
                prices["cny"] = text

            elif "درهم" in text:
                prices["aed"] = text

            elif "ریال عربستان" in text:
                prices["sar"] = text


        # طلای ۱۸ عیار
        gold18 = soup.find(
            string=lambda x:
            x and "طلای 18 عیار" in x
        )

        if gold18:
            prices["gold_18"] = gold18.parent.parent.get_text(
                " ",
                strip=True
            )


        # اونس جهانی
        ounce = soup.find(
            string=lambda x:
            x and "اونس" in x
        )

        if ounce:
            prices["gold_ounce"] = ounce.parent.parent.get_text(
                " ",
                strip=True
            )


    except Exception as e:
        print("TGJU Error:", e)


    return prices



# ==========================
# CoinGecko
# ==========================

def get_crypto_prices():

    coins = {
        "tether": "🪙 تتر (USDT)",
        "bitcoin": "🔶 بیت‌کوین (BTC)",
        "ethereum": "🔷 اتریوم (ETH)",
        "binancecoin": "🟡 بایننس کوین (BNB)",
        "solana": "🟣 سولانا (SOL)",
        "ripple": "⚫ ریپل (XRP)",
        "the-open-network": "🔵 تون‌کوین (TON)",
        "dogecoin": "🐶 دوج‌کوین (DOGE)"
    }


    result = {}


    try:

        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids="
            + ",".join(coins.keys())
            +
            "&vs_currencies=usd"
        )


        headers = {}

        if COINGECKO_API_KEY:
            headers["x-cg-demo-api-key"] = COINGECKO_API_KEY


        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        data = response.json()


        for key, title in coins.items():

            try:
                result[key] = format_usd(
                    data[key]["usd"]
                )

            except:
                result[key] = "نامشخص"


    except Exception as e:
        print("CoinGecko Error:", e)


    return result
    # ==========================
# Build Message
# ==========================

def create_message(tgju, crypto):

    message = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا:
{tgju['usd']}

💶 یورو اروپا:
{tgju['eur']}

💷 پوند انگلیس:
{tgju['gbp']}

🇨🇳 یوان چین:
{tgju['cny']}

🇦🇪 درهم امارات:
{tgju['aed']}

🇸🇦 ریال عربستان:
{tgju['sar']}


🥇 اونس جهانی طلا:
{tgju['gold_ounce']}

🥇 طلای ۱۸ عیار:
{tgju['gold_18']}

🥇 طلای ۲۴ عیار:
{tgju['gold_24']}


🪙 تتر (USDT):
{crypto.get('tether','نامشخص')}

🔶 بیت‌کوین (BTC):
{crypto.get('bitcoin','نامشخص')}

🔷 اتریوم (ETH):
{crypto.get('ethereum','نامشخص')}

🟡 بایننس کوین (BNB):
{crypto.get('binancecoin','نامشخص')}

🟣 سولانا (SOL):
{crypto.get('solana','نامشخص')}

⚫ ریپل (XRP):
{crypto.get('ripple','نامشخص')}

🔵 تون‌کوین (TON):
{crypto.get('the-open-network','نامشخص')}

🐶 دوج‌کوین (DOGE):
{crypto.get('dogecoin','نامشخص')}


🗓 تاریخ:
{get_jalali_date()}
"""


    return message



# ==========================
# Send Telegram Message
# ==========================

async def send_message():

    tgju_prices = get_tgju_prices()

    crypto_prices = get_crypto_prices()


    text = create_message(
        tgju_prices,
        crypto_prices
    )


    try:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=text
        )

        print(
            "Message sent successfully"
        )

    except Exception as e:
        print(
            "Telegram Error:",
            e
        )



# ==========================
# Run
# ==========================

if __name__ == "__main__":

    import asyncio

    asyncio.run(
        send_message()
    )
