# menu_pricing/middleware/error_handling.py
import logging
from django.http import JsonResponse
from menu_pricing.utils.Logging_config import WeatherAPIError, GooglePlacesAPIError, PricingError

logger = logging.getLogger(__name__)

class APIErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        """Handle exceptions and return appropriate responses."""
        if isinstance(exception, WeatherAPIError):
            logger.error(f"Weather API Error: {str(exception)}")
            return JsonResponse({
                'error': 'Weather service temporarily unavailable',
                'details': str(exception)
            }, status=503)
            
        elif isinstance(exception, GooglePlacesAPIError):
            logger.error(f"Google Places API Error: {str(exception)}")
            return JsonResponse({
                'error': 'Restaurant data service temporarily unavailable',
                'details': str(exception)
            }, status=503)
            
        elif isinstance(exception, PricingError):
            logger.error(f"Pricing Calculation Error: {str(exception)}")
            return JsonResponse({
                'error': 'Unable to calculate prices at this time',
                'details': str(exception)
            }, status=500)
            
        # Let Django handle other exceptions
        return None