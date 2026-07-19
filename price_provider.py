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
            r"طلای ۱۸ عیار\s*([\d,]+)",

            "mithqal":
            r"مثقال طلا\s*([\d,]+)",

            "emami":
            r"سکه امامی\s*([\d,]+)",


            "usd":
            r"دلار\s*([\d,]+)",

            "eur":
            r"یورو\s*([\d,]+)",

            "gbp":
            r"پوند انگلیس\s*([\d,]+)",

            "aed":
            r"درهم امارات\s*([\d,]+)",

            "sar":
            r"ریال عربستان\s*([\d,]+)",

            "try":
            r"لیر ترکیه\s*([\d,]+)",

            "cny":
            r"یوان چین\s*([\d,]+)",

            "usdt":
            r"تتر\s*([\d,]+)"
        }



        for key in keys:

            result = re.search(
                patterns[key],
                text
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

        prices.update(
            get_crypto()
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
