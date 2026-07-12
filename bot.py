import os, requests, pytz
from datetime import datetime
from khayyam import JalaliDatetime
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHANNEL = "@CryptoBrew"

bot = Bot(TOKEN)


def num(x):
    try:
        return f"{int(x):,}"
    except:
        return "نامشخص"


def time():
    now = datetime.now(pytz.timezone("Asia/Tehran"))
    return JalaliDatetime(now).strftime("%Y/%m/%d %H:%M")


def bonbast():
    try:
        from bonbast import Bonbast
        b = Bonbast()

        return {
            "usd": b.usd,
            "eur": b.eur,
            "gbp": b.gbp,
            "cny": b.cny,
            "aed": b.aed,
            "sar": b.sar,
            "gold18": b.gold18,
            "gold24": b.gold24,
            "coin": b.coin,
            "ounce": b.ounce
        }
    except:
        return {}


def crypto():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids":
        "bitcoin,ethereum,solana,ripple,cardano,tron,tether",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    headers = {
        "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
    }

    return requests.get(
        url,
        params=params,
        headers=headers
    ).json()


def c(data, name, icon):
    try:
        p = data[name]["usd"]
        ch = data[name]["usd_24h_change"]

        return f"{icon} {name.upper()}: ${num(p)} ({ch:.2f}%)"
    except:
        return f"{icon} {name.upper()}: نامشخص"


b = bonbast()
cdata = crypto()


msg = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {num(b.get('usd'))} تومان
💶 یورو اروپا: {num(b.get('eur'))} تومان
💷 پوند انگلیس: {num(b.get('gbp'))} تومان
🇨🇳 یوان چین: {num(b.get('cny'))} تومان
🇦🇪 درهم امارات: {num(b.get('aed'))} تومان
🇸🇦 ریال عربستان: {num(b.get('sar'))} تومان

🥇 اونس جهانی طلا: {num(b.get('ounce'))} تومان
🥇 طلای ۱۸ عیار: {num(b.get('gold18'))} تومان
🥇 طلای ۲۴ عیار: {num(b.get('gold24'))} تومان
🪙 سکه: {num(b.get('coin'))} تومان

{c(cdata,'bitcoin','🔶')}
{c(cdata,'ethereum','🔷')}
{c(cdata,'solana','🔸')}
{c(cdata,'ripple','🔹')}
{c(cdata,'cardano','🔸')}
{c(cdata,'tron','🔹')}
{c(cdata,'tether','💵')}

⏰ زمان بروزرسانی:
{time()}

➖➖➖➖➖➖➖
@CryptoBrew
"""


bot.send_message(
    chat_id=CHANNEL,
    text=msg
)
