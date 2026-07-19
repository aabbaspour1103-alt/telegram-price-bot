import requests
from bs4 import BeautifulSoup
import re


URL = "https://www.tgju.org"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean_number(value):
    try:
        return int(
            re.sub(r"[^\d]", "", value)
        )
    except:
        return None



def get_prices():

    prices = {}

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
            URL,
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        text = soup.get_text(
            " ",
            strip=True
        )


        patterns = {

            # طلا و سکه
            "gold18": [
                r"طلا ۱۸\s+([\d,]+)",
                r"طلای ۱۸ عیار\s+([\d,]+)"
            ],

            "mithqal": [
                r"مثقال طلا\s+([\d,]+)"
            ],

            "emami": [
                r"سکه\s+([\d,]+)"
            ],


            # ارز
            "usd": [
                r"دلار\s+([\d,]+)"
            ],

            "eur": [
                r"یورو\s+([\d,]+)"
            ],

            "gbp": [
                r"پوند(?: انگلیس)?\s+([\d,]+)",
                r"پوند\s*انگلیس\s+([\d,]+)"
            ],

            "aed": [
                r"درهم امارات\s+([\d,]+)",
                r"درهم\s+([\d,]+)"
            ],

            "sar": [
                r"ریال عربستان\s+([\d,]+)"
            ],

            "try": [
                r"لیر ترکیه\s+([\d,]+)"
            ],

            "cny": [
                r"یوان چین\s+([\d,]+)"
            ],


            # کریپتو
            "usdt": [
                r"تتر\s+([\d,]+)"
            ]
        }


        for key in keys:

            prices[key] = None

            for pattern in patterns[key]:

                result = re.search(
                    pattern,
                    text
                )

                if result:

                    prices[key] = clean_number(
                        result.group(1)
                    )

                    break


    except Exception as e:

        print(
            "TGJU Error:",
            e
        )

        for key in keys:
            prices[key] = None


    return prices



if __name__ == "__main__":

    data = get_prices()

    print(data)
