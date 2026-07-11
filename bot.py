def get_prices():

    url = "https://api.navasan.tech/api/"

    headers = {
        "Api-Key": NAVASAN_API_KEY
    }

    response = requests.get(url, headers=headers)

    print("STATUS:", response.status_code)
    print("TEXT:")
    print(response.text)

    return "تست API"
