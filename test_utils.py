from django.test import TestCase
from menu_pricing.utils.weather import fetch_weather_data
from menu_pricing.utils.google_maps import fetch_google_places_data, fetch_google_places_busy_times
from menu_pricing.utils.pricing import adjust_price

class UtilsTestCase(TestCase):
    def test_fetch_weather_data(self):
        latitude = 40.7643
        longitude = -73.5252
        weather_data = fetch_weather_data(latitude, longitude)
        self.assertIsNotNone(weather_data)
        print("Weather Data:", weather_data)

    def test_google_places_data(self):
        api_key = "AIzaSyAnoTGAUSoT0HRcwk8BNZOwzWuQUaSu56A^X"
        latitude = 40.7643
        longitude = -73.5252
        nearby_restaurants = fetch_google_places_data(api_key, latitude, longitude, radius=2000)
        self.assertIsInstance(nearby_restaurants, list)
        print("Nearby Restaurants:", nearby_restaurants)

    def test_busy_times(self):
        api_key = "AIzaSyAnoTGAUSoT0HRcwk8BNZOwzWuQUaSu56A^X"
        place_id = "ChIJb9Mi7uKAwokRS1HIeKuO13o"
        busy_times = fetch_google_places_busy_times(api_key, place_id)
        self.assertIsNotNone(busy_times)
        print("Busy Times:", busy_times)

    def test_adjust_price(self):
        adjusted_price = adjust_price(
            item_price=12.0,
            temperature=75.0,
            rain_chance="clear",
            busy_status="moderate",
            competitive_price=10.0
        )
        self.assertGreaterEqual(adjusted_price, 0)
        print("Adjusted Price:", adjusted_price)
