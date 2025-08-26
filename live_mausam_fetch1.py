import requests
import pymongo
import datetime
import time

# 🔹 MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["live_weather_db"]
collection = db["live_weather_data"]

# 🔹 OpenWeather API Key
api_key = "458adbbfcc1478797383ff209d07a898"

# 🔹 Cities to track
cities = [
    "New Delhi", "Mumbai", "Kolkata", "Chennai", "Bengaluru", "Hyderabad", "Gandhinagar", "Jaipur", "Lucknow",
    "Bhopal", "Patna", "Raipur", "Ranchi", "Bhubaneswar", "Thiruvananthapuram", "Panaji", "Shimla", "Dehradun",
    "Imphal", "Shillong", "Aizawl", "Kohima", "Itanagar", "Dispur", "Agartala", "Gangtok", "Chandigarh"
]

# 🔹 Weather thresholds for alerts
TEMP_HIGH = 35  # Celsius
TEMP_LOW = 5  # Celsius
ALERT_WEATHER = [
    "Thunderstorm", "Drizzle", "Rain", "Snow", "Mist", "Smoke", "Haze", "Dust", "Fog", "Sand", "Ash", "Squall",
    "Tornado", "Extreme"
]

def fetch_and_store_weather():
    """Fetch live weather data for multiple cities and store it in MongoDB."""
    for city in cities:
        try:
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
            response.raise_for_status()
            json_file = response.json()
            
            # Extract weather data
            city_name = json_file['name']
            country_name = json_file['sys']['country']
            k_temperature = json_file['main']['temp']
            c_temperature = round(k_temperature - 273.15, 2)
            humidity = json_file['main']['humidity']  # ✅ Added Humidity
            pressure = json_file['main']['pressure']  # ✅ Added Pressure
            wind_speed = json_file['wind']['speed']  # ✅ Added Wind Speed
            weather_display = json_file['weather'][0]['main']
            
            # Prepare data for MongoDB
            weather_data = {
                "city": city_name,
                "country": country_name,
                "temperature_C": c_temperature,
                "humidity": humidity,
                "pressure_hPa": pressure,
                "wind_speed_mps": wind_speed,
                "weather": weather_display,
                "date": datetime.datetime.utcnow()
            }

            # Insert only if a similar record does not exist
            existing_data = collection.find_one({"city": city_name, "date": {"$gte": datetime.datetime.utcnow()}})
            if not existing_data:
                collection.insert_one(weather_data)
                print(f"✅ Data Saved for {city}: {weather_data}")
            else:
                print(f"⚠️ Skipped {city}, Data already exists!")

            # Trigger Alerts
            check_alerts(city_name, c_temperature, weather_display, humidity, wind_speed)

        except Exception as e:
            print(f"❌ Error fetching weather for {city}: {e}")

def check_alerts(city, temperature, weather, humidity, wind_speed):
    """Trigger alerts for extreme weather conditions."""
    if temperature > TEMP_HIGH:
        print(f"🚨 ALERT: {city} is TOO HOT! 🌡️ {temperature}°C")
    elif temperature < TEMP_LOW:
        print(f"🚨 ALERT: {city} is TOO COLD! ❄️ {temperature}°C")
    
    if weather in ALERT_WEATHER:
        print(f"⚠️ WARNING: Extreme Weather in {city} - {weather}")

    if humidity > 90:
        print(f"💧 ALERT: High Humidity in {city}! ({humidity}%)")

    if wind_speed > 15:
        print(f"🌬️ ALERT: Strong Winds in {city}! ({wind_speed} m/s)")

# 🔹 Fetch live data every 45 seconds
while True:
    fetch_and_store_weather()
    time.sleep(45)  # Fetch every 45 seconds
