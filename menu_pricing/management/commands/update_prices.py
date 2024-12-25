from django.core.management.base import BaseCommand
from menu_pricing.utils import fetch_weather_data, fetch_google_places_data, fetch_google_places_busy_times, calculate_dynamic_price

class Command(BaseCommand):
    help = "Fetch data and update menu prices dynamically"

    def handle(self, *args, **kwargs):
        location = (40.7128, -74.0060)  # Example coordinates for New York
        google_api_key = "YOUR_GOOGLE_API_KEY"
        openweather_api_key = "YOUR_OPENWEATHER_API_KEY"
        place_id = "ChIJb9Mi7uKAwokRS1HIeKuO13o"  # Example Place ID for the restaurant

        try:
            # Fetch weather data
            weather_data = fetch_weather_data(location, openweather_api_key)
            print("Weather Data:", weather_data)  # Debug print

            # Fetch busy times data from Google Places
            busy_times_data = fetch_google_places_busy_times(google_api_key, place_id)
            print("Busy Times Data:", busy_times_data)  # Debug print

            # Fetch competitor data (use Google Places or another API)
            competitor_data = fetch_google_places_data("restaurants", location, google_api_key)
            print("Competitor Data:", competitor_data)  # Debug print

            # Example base price for a menu item
            base_price = 10.0

            # Calculate the lowest competitive price
            competitor_prices = [item.get('price', base_price) for item in competitor_data.get('results', [])]
            lowest_price = min(competitor_prices) if competitor_prices else base_price

            # Calculate dynamic price based on weather, busy times, and competitor data
            new_price = calculate_dynamic_price(base_price, weather_data, busy_times_data, competitor_data, lowest_price)
            self.stdout.write(self.style.SUCCESS(f"Updated price: {new_price}"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))
