import requests
from decouple import config


url = "http://127.0.0.1:8000/academia/schools/ng"
api_key = config("API_KEY")
api_key_two = config("API_KEY_TWO")

headers = {
    "accept": "application/json",
    "authorization": f"Api-Key {api_key}",
}

headers_two = {
    "accept": "application/json",
    "authorization": f"Api-Key {api_key_two}",
}


def run_abram():
    for i in range(60):
        r = requests.get(url, headers=headers)
        print(f"Status Code for Abram {i+1}: {r.status_code}")


def run_faraday():
    for i in range(40):
        r = requests.get(url, headers=headers_two)
        print(f"Status Code for Faraday {i+1}: {r.status_code}")