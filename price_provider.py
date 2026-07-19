import requests
from bs4 import BeautifulSoup


URL = "https://www.tgju.org"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def test_page():

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=20
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # جستجوی کلمات مهم در صفحه
    keywords = [
        "dollar",
        "price_dollar",
        "سکه",
        "دلار",
        "طلا"
    ]

    for word in keywords:
        print("\nSEARCH:", word)

        result = soup.find_all(
            string=lambda text: text and word in text
        )

        print("FOUND:", len(result))

        for item in result[:3]:
            print(item.strip())


if __name__ == "__main__":
    test_page()
