from typing import Dict

def adjust_price(base_price, temperature, rain_chance, busy_status, competitive_price):
    weather_factor = 1.0
    if temperature < 10:
        weather_factor += 0.1
    if 'rain' in rain_chance.lower():
        weather_factor += 0.15

    busy_factor = 1.0
    if busy_status['current_popularity'] > 80:
        busy_factor += 0.2

    adjusted_price = base_price * weather_factor * busy_factor
    adjusted_price = max(adjusted_price, competitive_price)
    return round(adjusted_price, 2)
