import requests
from decouple import config


url = "http://127.0.0.1:8000/academia/schools/ng"
api_key = config("API_KEY")
headers = {
    "accept": "application/json",
    "authorization": f"Api-Key {api_key}",
}

for i in range(100):
    r = requests.get(url, headers=headers)
    print(f"Status Code {i+1}: {r.status_code}")
