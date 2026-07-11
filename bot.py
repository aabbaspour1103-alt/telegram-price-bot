import os
import requests

TOKEN = os.getenv("TOKEN")

print("TOKEN:", TOKEN)

url = f"https://api.telegram.org/bot{TOKEN}/getMe"

r = requests.get(url)

print(r.text)
