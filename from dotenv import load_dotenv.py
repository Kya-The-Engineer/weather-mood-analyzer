from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")

url = f"https://www.openweathermap.org/3.0/onecall"

params = {
    "lat": 33.7501,
    "lon": 84.3885,
    "appid": API_KEY,
}

response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    daily = data.get("daily")
    daily_sunset = daily.get("daily_sunset")

    print("Daily Sunset in Atlanta GA:", daily_sunset)

else :
    print("Error:", response.status_code)

    