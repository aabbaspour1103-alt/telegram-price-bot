import os
import asyncio
from datetime import datetime

import pytz
import jdatetime
from telegram import Bot

from price_provider import get_prices


TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"


def format_number(value, crypto=False):
    try:
        if value is None:
            return "نامشخص"

        num = float(value)

        if not crypto:
            num = num / 10   # ریال به تومان

        if crypto:
            if num >= 1000:
                return f"{num:,.2f}"
            elif num >= 1:
                return f"{num:,.4f}".rstrip("0").rstrip(".")
            else:
                return f"{num:,.6f}".rstrip("0").rstrip(".")

        return f"{int(num):,}"

    except:
        return "نامشخص"


def change_text(value):
    try:
        if value is None:
            return ""

        value = float(value)

        if value > 0:
            return f" 🔺+{value:.2f}%"

        elif value < 0:
            return f" 🔻{value:.2f}%"

        return " ➖0.00%"

    except:
        return ""


def iran_time():

    try:
        tz = pytz.timezone("Asia/Tehran")
        now = datetime.now(tz)

        j = jdatetime.datetime.fromgregorian(
            datetime=now
        )

        return j.strftime("%Y/%m/%d - %H:%M")

    except:
        return "نامشخص"



def safe_price(data, key):
    try:
        return data.get(key)
    except:
        return None



def create_message():

    try:
        money = get_prices()

        if not isinstance(money, dict):
            money = {}

    except Exception as e:
        print("Price Provider Error:", e)
        money = {}


    return f"""
💰 قیـمت لحظه‌ای بازار

🥈 ارز :

💵 دلار آمریکـــــــا: {format_number(safe_price(money,'usd'))} تومان{change_text(safe_price(money,'usd_change'))}

💶 یــــورو اروپـــا: {format_number(safe_price(money,'eur'))} تومان{change_text(safe_price(money,'eur_change'))}

💷 پـــوند انگلیس: {format_number(safe_price(money,'gbp'))} تومان{change_text(safe_price(money,'gbp_change'))}

🇨🇳 یــــوان چـــین: {format_number(safe_price(money,'cny'))} تومان

🇦🇪 درهــم امارات: {format_number(safe_price(money,'aed'))} تومان

🇸🇦 ریال عربستان: {format_number(safe_price(money,'sar'))} تومان

🇹🇷 لـــــیــــر ترکیه: {format_number(safe_price(money,'try'))} تومان


🥇 طلا و سکه:

🥇 طلای ۱۸ عیار: {format_number(safe_price(money,'gold18'))} تومان

🟡 مثقال طلا: {format_number(safe_price(money,'mithqal'))} تومان

🪙 سکه امامی: {format_number(safe_price(money,'emami'))} تومان


🥇 ارز دیجیتال:

🔶 بیت‌کوین (BTC): {format_number(safe_price(money,'btc'),True)} دلار{change_text(safe_price(money,'btc_change'))}

🔷 اتریوم (ETH): {format_number(safe_price(money,'eth'),True)} دلار{change_text(safe_price(money,'eth_change'))}

🔸 بایننس‌کوین (BNB): {format_number(safe_price(money,'bnb'),True)} دلار{change_text(safe_price(money,'bnb_change'))}

🔹 سولانا (SOL): {format_number(safe_price(money,'sol'),True)} دلار{change_text(safe_price(money,'sol_change'))}

🔸 ریپل (XRP): {format_number(safe_price(money,'xrp'),True)} دلار{change_text(safe_price(money,'xrp_change'))}

🔹 تون‌کوین (TON): {format_number(safe_price(money,'ton'),True)} دلار{change_text(safe_price(money,'ton_change'))}

🔸 دوج‌کوین (DOGE): {format_number(safe_price(money,'doge'),True)} دلار{change_text(safe_price(money,'doge_change'))}

💵 تتر (USDT): {format_number(safe_price(money,'usdt'),True)} دلار


🕒 بروزرسانی:
{iran_time()}

- @CryptoBrew
"""


async def main():

    try:

        if not TOKEN:
            print("TOKEN not found")
            return

        bot = Bot(token=TOKEN)

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=create_message()
        )

        print("Message sent successfully")

    except Exception as e:

        print(
            "Telegram Error:",
            e
        )


if __name__ == "__main__":
    asyncio.run(main())
