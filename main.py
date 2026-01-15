import requests

API_KEY = "YOUR_API_KEY"
lat = 32.7767
lon = 96.7970 # Dallas Coordinates


url = f"https://api.openweathermap.org/data/3.0/onecall"

params = {
    "lat": lat,
    "lon": lon,
    "appid": API_KEY,
    "units": "imperial",    

}

response = requests.get(url, params=params, timeout=15)
response.raise_for_status()

data = response.json()
print(data)


