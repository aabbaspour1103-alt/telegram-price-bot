import requests
from bs4 import BeautifulSoup

URL = "https://www.tgju.org"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

def get_html():
    response = requests.get(URL, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


if __name__ == "__main__":
    soup = get_html()
    print(soup.title.text)
