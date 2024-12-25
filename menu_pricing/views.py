
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from menu_pricing.utils.google_maps import get_place_details, get_nearby_restaurants
from menu_pricing.utils.weather import get_weather_data
from menu_pricing.utils.pricing import adjust_price
from menu_pricing.utils.maps import get_place_busyness

def home(request):
    context = {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'menu_pricing/index.html',context)

def get_location_details(request):
    """Handle both restaurant and non-restaurant location clicks"""
    lat = float(request.GET.get('lat'))
    lng = float(request.GET.get('lng'))
    
    # First, check if clicked location is a restaurant
    place_details = get_place_details(lat, lng)
    
    if place_details and 'restaurant' in place_details.get('types', []):
        # Location is a restaurant - get detailed information
        weather_data = get_weather_data(lat, lng)
        busyness_data = get_place_busyness(place_details['place_id'])
        
        # Get and adjust menu prices
        base_menu = [
            {"name": "Pizza", "base_price": 10},
            {"name": "Burger", "base_price": 8},
            {"name": "Pasta", "base_price": 12},
        ]
        
        adjusted_menu = []
        for item in base_menu:
            adjusted_price = adjust_price(
                item['base_price'],
                weather_data['temperature'],
                weather_data['rain_chance'],
                busyness_data,
                competitive_price=7.5  # This could be fetched from a database
            )
            adjusted_menu.append({
                "name": item['name'],
                "price": adjusted_price
            })
        
        return JsonResponse({
            'is_restaurant': True,
            'restaurant_details': {
                'name': place_details['name'],
                'address': place_details['formatted_address'],
                'weather': weather_data,
                'busyness': busyness_data['current_popularity'],
                'status': place_details['business_status'],
                'menu_items': adjusted_menu
            }
        })
    else:
        # Location is not a restaurant - find nearby restaurants
        nearby_restaurants = get_nearby_restaurants(lat, lng, radius=5000)
        
        if not nearby_restaurants:
            return JsonResponse({
                'is_restaurant': False,
                'message': 'No restaurants available within 5km radius'
            })
            
        return JsonResponse({
            'is_restaurant': False,
            'nearby_restaurants': [
                {
                    'name': r['name'],
                    'vicinity': r['vicinity'],
                    'lat': r['geometry']['location']['lat'],
                    'lng': r['geometry']['location']['lng']
                }
                for r in nearby_restaurants
            ]
        })