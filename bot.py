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



def get_crypto():

    return {}



def create_message():

    money = get_prices()

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


🥇 طلا و سکه:

🥇 طلای ۱۸ عیار: {format_number(money.get('gold18'))} تومان
🟡 مثقال طلا: {format_number(money.get('mithqal'))} تومان
🪙 سکه امامی: {format_number(money.get('emami'))} تومان


💵 تتر:
{format_number(money.get('usdt'))} تومان


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

    except Exception as e:

        print(
            "Telegram Error:",
            e
        )



if __name__ == "__main__":

    asyncio.run(main())
