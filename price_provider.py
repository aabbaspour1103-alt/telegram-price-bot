import requests
from bs4 import BeautifulSoup
import re


URL = "https://www.tgju.org"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean_number(value):
    return int(
        re.sub(r"[^\d]", "", value)
    )


def get_prices():

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=20
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    text = soup.get_text(
        " ",
        strip=True
    )


    prices = {}


    patterns = {
        "gold18": r"طلا ۱۸\s+([\d,]+)",
        "mithqal": r"مثقال طلا\s+([\d,]+)",
        "emami": r"سکه\s+([\d,]+)",
        "usd": r"دلار\s+([\d,]+)",
        "usdt": r"تتر\s+([\d,]+)"
    }


    for key, pattern in patterns.items():

        result = re.search(
            pattern,
            text
        )

        if result:
            prices[key] = clean_number(
                result.group(1)
            )
        else:
            prices[key] = None


    return prices



if __name__ == "__main__":

    data = get_prices()

    print(data)
