#Configuration and imports
#-------------------------
import os
from datetime import datetime #converts Unix to readable time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_GEOCODE_URL = "https://api.openweathermap.org/geo/1.0/direct" #This version require lat and lon
BASE_ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall" #overall onecall weather API 

#Helper functions
#-----------------
def to_local_time(unix_time: int) -> str:
    """Convert UNIX timestamp to a readable local time string."""
    return datetime.fromtimestamp(unix_time).strftime("%I:%M %p").lstrip("0")

def mood_from_weather(temp_f: float, clouds: int, wind_mph: float, humidity: int) -> str:
    """Determine mood based on weather conditions."""
    if temp_f >= 80 and clouds <= 40 and wind_mph <= 12:
        return "Golden Mood (sunny + warm)"
    if clouds >= 75 and humidity >= 70:
        return "Cozy & Moody (cloudy + humid)"
    if wind_mph >= 18:
        return "Windy Edge (hold onto your hat!)"
    if temp_f <= 45: 
        return "Chill Mode (bundle up!)"
    return "Balanced Vibes"

def outfit_tip(temp_f: float, clouds: int, wind_mph: float, hmumidity: int) -> str: 
    """Suggest outfit tips based on weather conditions."""
    if temp_f <= 45:
        return "Jacket, layers, and closed-toe shoes."
    if temp_f <= 60: 
        return "Light jacket or hoodie."
    if temp_f <=75: 
        return "T-shirt vibes. Bring a layer if you usually get cold."
    if wind_mph >= 18:
        return "Secure hair and clothes: it's breezy!"
    return "Light fit, stay hydrated!"

#API Functions
#-----------------    
def safe_get(d: dict, *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
        if cur is None:
            return default
    return cur

def geocode_city(city: str, state: str = "", country: str = "US"):
    if not API_KEY:
        raise ValueError("Missing API_KEY. Check your .env file.")
    q = f"{city},{state},{country}".strip(",")
    params = {"q": q, "limit": 1, "appid": API_KEY}

    r = requests.get(BASE_GEOCODE_URL, params=params, timeout=15)
    r.raise_for_status()

    results = r.json()
    if not results:
        raise ValueError(f"City not found: {q}")
    
    place = results[0]
    return place["lat"], place["lon"], place.get("name")

def get_onecall_weather(lat: float, lon: float, units: str = "imperial"):
    if not API_KEY:
        raise ValueError("Missing API_KEY. Check your .env file.")
    
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "imperial",
        "exclude": "minutely,alerts"
    }

    r = requests.get(BASE_ONECALL_URL, params=params, timeout=15)

    if r.status_code == 401:
        raise PermissionError("401 Unauthorized: API key is invalid, missing, or restricted.")
    if r.status_code == 404:
        raise FileNotFoundError("404 Not Found: Endpoint or request is incorrect.")
    r.raise_for_status()

    return r.json()

#Main Application
#-----------------  

def main():
    print("\n Weather Mood Analyzer\n" + "-" *28)

    city = input("Enter a city (example: Dallas): ").strip() 
    state = input("Enter a state abbreviations (example: TX): ").strip()

    try:
        lat, lon, place_name = geocode_city(city, state)
        data = get_onecall_weather(lat, lon)
    except Exception as e:
        print(f"Error: {e}")
        return

    current = data.get("current", {})
    daily = data.get("daily", [])

    temp = current.get("temp")
    feels_like = current.get("feels_like")
    humidity = current.get("humidity")
    wind_mph = current.get("wind_speed")
    clouds = current.get("clouds",0)
    sunrise = current.get("sunrise")
    sunset = current.get("sunset")

    today = daily[0] if daily else {}
    high = today.get("temp", {}).get("max")
    low = today.get("temp", {}).get("min")

    description = ""
    weather_list = current.get("weather", [{}])
    if weather_list:
        description = weather_list[0].get("description", "").title()

    mood = mood_from_weather(temp, clouds, wind_mph, humidity)
    outfit = outfit_tip(temp, clouds, wind_mph, humidity)

    print(f"\n Location: {place_name}")
    print(f"Current Weather: {description}")
    print(f"Temperature: {temp}°F (feels like {feels_like}°F)")
    print(f"Cloud Cover: {clouds}%")
    print(f"Wind Speed: {wind_mph} mph")
    print(f"Humidity: {humidity}%")
    print(f"High Today: {high}°F, Low Today: {low}°F")
    print(f"Mood: {mood}")
    print(f"Outfit Tip: {outfit}")

if __name__ == "__main__":
    main()
