import requests
import re
from bs4 import BeautifulSoup


TGJU_URL = "https://www.tgju.org"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=bitcoin,ethereum,binancecoin,solana,ripple,"
    "the-open-network,dogecoin,cardano,avalanche-2,"
    "polkadot,litecoin,shiba-inu,tether"
    "&vs_currencies=usd"
)


def clean_number(value):

    try:
        value = value.translate(
            str.maketrans(
                "۰۱۲۳۴۵۶۷۸۹",
                "0123456789"
            )
        )

        return int(
            re.sub(r"[^\d]", "", value)
        )

    except:
        return None



def get_tgju():

    data = {}

    keys = [
        "gold18",
        "mithqal",
        "emami",
        "usd",
        "eur",
        "gbp",
        "aed",
        "sar",
        "try",
        "cny",
        "usdt"
    ]


    try:

        response = requests.get(
            TGJU_URL,
            headers=HEADERS,
            timeout=15
        )


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        text = soup.get_text(
            " ",
            strip=True
        )


        patterns = {

            "gold18":
            r"(?:طلای\s*۱۸\s*عیار|طلای\s*18\s*عیار|گرم طلای ۱۸|طلای هجده عیار)\s*[:\-]?\s*([\d,]+)",


            "mithqal":
            r"(?:مثقال طلا|مثقال)\s*[:\-]?\s*([\d,]+)",


            "emami":
            r"(?:سکه امامی|امامی)\s*[:\-]?\s*([\d,]+)",


            "usd":
            r"(?:دلار آمریکا|دلار)\s*[:\-]?\s*([\d,]+)",


            "eur":
            r"یورو\s*[:\-]?\s*([\d,]+)",


            "gbp":
            r"پوند انگلیس\s*[:\-]?\s*([\d,]+)",


            "aed":
            r"درهم امارات\s*[:\-]?\s*([\d,]+)",


            "sar":
            r"ریال عربستان\s*[:\-]?\s*([\d,]+)",


            "try":
            r"لیر ترکیه\s*[:\-]?\s*([\d,]+)",


            "cny":
            r"یوان چین\s*[:\-]?\s*([\d,]+)",


            "usdt":
            r"(?:تتر|Tether|USDT)\s*[:\-]?\s*([\d,]+)"
        }



        for key in keys:

            result = re.search(
                patterns[key],
                text,
                re.IGNORECASE
            )


            if result:

                data[key] = clean_number(
                    result.group(1)
                )

            else:

                data[key] = None



    except Exception as e:

        print(
            "TGJU ERROR:",
            e
        )

        for key in keys:
            data[key] = None



    return data




def get_crypto():

    data = {}


    coins = {

        "btc": "bitcoin",
        "eth": "ethereum",
        "bnb": "binancecoin",
        "sol": "solana",
        "xrp": "ripple",
        "ton": "the-open-network",
        "doge": "dogecoin",
        "ada": "cardano",
        "avax": "avalanche-2",
        "dot": "polkadot",
        "ltc": "litecoin",
        "shib": "shiba-inu",
        "usdt": "tether"

    }


    try:

        response = requests.get(
            COINGECKO_URL,
            timeout=15
        )


        result = response.json()


        for name, coin_id in coins.items():

            coin = result.get(
                coin_id,
                {}
            )

            data[name] = coin.get(
                "usd"
            )


    except Exception as e:

        print(
            "COINGECKO ERROR:",
            e
        )


    return data




def get_prices():

    prices = {}


    try:

        prices.update(
            get_tgju()
        )

    except Exception as e:

        print(
            "TGJU FAIL:",
            e
        )


    try:

        crypto = get_crypto()

        prices.update(
            crypto
        )


        # اگر تتر تومان از TGJU پیدا نشد
        # تبدیل تتر دلاری به تومان

        if not prices.get("usdt"):

            if crypto.get("usdt") and prices.get("usd"):

                prices["usdt"] = int(
                    crypto["usdt"] * prices["usd"]
                )


    except Exception as e:

        print(
            "CRYPTO FAIL:",
            e
        )


    return prices




if __name__ == "__main__":

    print(
        get_prices()
    )
