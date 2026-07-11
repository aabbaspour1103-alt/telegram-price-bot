import requests

TOKEN = "توکن_ربات_خودت"

url = f"https://api.telegram.org/bot{TOKEN}/getMe"

r = requests.get(url)

print(r.text)
