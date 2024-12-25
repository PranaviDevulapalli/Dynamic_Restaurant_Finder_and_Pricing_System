import requests

def get_weather_data(lat, lng):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid=24f8f1b4c2cb6a0d267f114c5384c852"
    response = requests.get(url)
    data = response.json()
    
    temperature = data['main']['temp'] - 273.15  # Kelvin to Celsius
    rain_chance = data['weather'][0]['description']
    return {'temperature': temperature, 'rain_chance': rain_chance}
