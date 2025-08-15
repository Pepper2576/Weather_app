import requests

def fetch_weather(long, lat):
    weather_endpoint = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m'
    response = requests.get(weather_endpoint)
    if response.status_code == 200:
        print("Weather data fetched successfully.")
        weather_data = response.json()
        data = {
            "latitude": lat,
            "longitude": long,
            "time": weather_data['current']['time'],
            "temperature": weather_data['current']['temperature_2m']
            }
        return data
    else:
        return {"error": "Failed to fetch weather data"}

if __name__ == "__main__":
    fetch_weather()