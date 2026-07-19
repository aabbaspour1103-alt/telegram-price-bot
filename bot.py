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
                return f"{num:,.3f}".rstrip("0").rstrip(".")

            else:
                return f"{num:,.6f}".rstrip("0").rstrip(".")

        return f"{int(num):,}"

    except:
        return "نامشخص"



def iran_time():

    try:
        tz = pytz.timezone(
            "Asia/Tehran"
        )

        now = datetime.now(tz)

        j = jdatetime.datetime.fromgregorian(
            datetime=now
        )

        return j.strftime(
            "%Y/%m/%d - %H:%M"
        )

    except:
        return "نامشخص"



def create_message():

    try:
        data = get_prices()

        if not isinstance(data, dict):
            data = {}

    except:
        data = {}


    return f"""
💰 قیـمت لحظه‌ای بازار

🥈 ارز :

💵 دلار آمریکـــــــا: {format_number(data.get('usd'))} تومان
💶 یــــورو اروپـــا: {format_number(data.get('eur'))} تومان
💷 پـــوند انگلیس: {format_number(data.get('gbp'))} تومان
🇨🇳 یــــوان چـــین: {format_number(data.get('cny'))} تومان
🇦🇪 درهــم امارات: {format_number(data.get('aed'))} تومان
🇸🇦 ریال عربستان: {format_number(data.get('sar'))} تومان
🇹🇷 لـــــیــــر ترکیه: {format_number(data.get('try'))} تومان


🥇 طلا و سکه:

🟡 طلای ۱۸ عـیار: {format_number(data.get('gold18'))} تومان
🟡 مثــــــقال طلا: {format_number(data.get('mithqal'))} تومان
🟡 ســــکه امامی: {format_number(data.get('emami'))} تومان

💵 تـــــــــــــــــتــر: {format_number(data.get('usdt'))} تومان


🥇 ارز دیجیتال:

🔶 بیــــت‌کوین (BTC): {format_number(data.get('btc'), True)} دلار

🔷 اتــــریــــــوم (ETH): {format_number(data.get('eth'), True)} دلار

🔸 بایننس‌کوین (BNB): {format_number(data.get('bnb'), True)} دلار

🔹 ســــــــــولانا (SOL): {format_number(data.get('sol'), True)} دلار

🔸 ریـــــــــــــپل (XRP): {format_number(data.get('xrp'), True)} دلار

🔹 تـــــون‌کوین (TON): {format_number(data.get('ton'), True)} دلار

🔸 دوج‌کـوین (DOGE): {format_number(data.get('doge'), True)} دلار

🔹 کـــاردانــــــو (ADA): {format_number(data.get('ada'), True)} دلار

🔸 آوالانـــــــچ (AVAX): {format_number(data.get('avax'), True)} دلار

🔹 پولـــکـــادات (DOT): {format_number(data.get('dot'), True)} دلار

🔸 لایــــــت‌کوین (LTC): {format_number(data.get('ltc'), True)} دلار

🔹 شیـــــبا اینو (SHIB): {format_number(data.get('shib'), True)} دلار


🕒 بــروزرسانــی:
{iran_time()}

- @CryptoBrew
"""



async def main():

    try:

        bot = Bot(
            token=TOKEN
        )

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=create_message()
        )

        print("Sent")

    except Exception as e:

        print(
            "Telegram Error:",
            e
        )



if __name__ == "__main__":

    asyncio.run(main())
