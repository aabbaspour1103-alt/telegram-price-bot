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

    # فقط لینک‌ها و المان‌هایی که احتمالاً قیمت دارند
    items = soup.find_all(
        ["tr", "div", "span"],
        limit=200
    )

    for item in items:
        text = item.get_text(" ", strip=True)

        if any(word in text for word in [
            "دلار",
            "یورو",
            "طلا",
            "سکه"
        ]):
            print("------------------")
            print(text[:300])


if __name__ == "__main__":
    test_page()
