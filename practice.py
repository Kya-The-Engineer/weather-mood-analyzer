from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")

url = f"https://api.openweathermap.org/data/3.0/onecall"

params = {
    "lat": 33.7501,
    "lon": 84.3885,
    "appid": API_KEY,
    "units": "imperial"
}

response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    current = data.get("current", {})
    current_temp = current.get("temp")

    print("Current Temp in Atlanta GA:", current_temp)

else :
    print("Error:", response.status_code)
