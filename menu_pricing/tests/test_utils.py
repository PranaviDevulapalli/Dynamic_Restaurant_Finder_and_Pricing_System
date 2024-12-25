# menu_pricing/tests/test_utils.py
import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.conf import settings
from menu_pricing.utils import (
    fetch_weather_data,
    fetch_google_places_data,
    fetch_google_places_busy_times,
    adjust_price
)

class WeatherUtilsTests(TestCase):
    @patch('requests.get')
    def test_fetch_weather_data_success(self, mock_get):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'main': {'temp': 293.15, 'humidity': 70},
            'weather': [{'main': 'Rain', 'description': 'light rain'}],
            'wind': {'speed': 5.1}
        }
        mock_get.return_value = mock_response

        result = fetch_weather_data(40.7643, -73.5252, 'test_api_key')
        
        self.assertEqual(result['temperature'], 293.15)
        self.assertEqual(result['conditions'], 'Rain')
        
    @patch('requests.get')
    def test_fetch_weather_data_api_error(self, mock_get):
        # Mock API error
        mock_get.side_effect = Exception('API Error')
        
        with self.assertRaises(Exception) as context:
            fetch_weather_data(40.7643, -73.5252, 'test_api_key')
        
        self.assertTrue('Weather service unavailable' in str(context.exception))

class GooglePlacesUtilsTests(TestCase):
    @patch('requests.get')
    def test_fetch_places_data_success(self, mock_get):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [
                {
                    'name': 'Test Restaurant',
                    'place_id': 'test123',
                    'rating': 4.5,
                    'vicinity': '123 Test St'
                }
            ]
        }
        mock_get.return_value = mock_response

        result = fetch_google_places_data('test_api_key', 40.7643, -73.5252)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Test Restaurant')
        
    @patch('requests.get')
    def test_fetch_busy_times_success(self, mock_get):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'result': {
                'current_opening_hours': {'open_now': True},
                'popular_times': {'current_popularity': 75}
            }
        }
        mock_get.return_value = mock_response

        result = fetch_google_places_busy_times('test_api_key', 'test_place_id')
        
        self.assertTrue(result['is_open'])
        self.assertEqual(result['current_popularity'], 75)

class PricingUtilsTests(TestCase):
    def test_adjust_price_cold_weather(self):
        result = adjust_price(
            item_price=10.0,
            temperature=40.0,  # Cold weather
            rain_chance='Clear',
            busy_status={'current_popularity': 50},
            competitive_price=9.0
        )
        self.assertGreater(result, 10.0)  # Price should increase
        
    def test_adjust_price_rainy_weather(self):
        result = adjust_price(
            item_price=10.0,
            temperature=65.0,
            rain_chance='Rain',
            busy_status={'current_popularity': 50},
            competitive_price=9.0
        )
        self.assertGreater(result, 10.0)  # Price should increase
        
    def test_adjust_price_busy_time(self):
        result = adjust_price(
            item_price=10.0,
            temperature=65.0,
            rain_chance='Clear',
            busy_status={'current_popularity': 85},  # Very busy
            competitive_price=9.0
        )
        self.assertGreater(result, 10.0)  # Price should increase

if __name__ == '__main__':
    unittest.main()