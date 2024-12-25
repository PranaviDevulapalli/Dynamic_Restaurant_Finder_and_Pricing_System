# utils/google_maps.py
import requests
from django.conf import settings

def get_place_details(lat, lng):
    """Check if a location is a restaurant and get its details"""
    # First, find the nearest place to the clicked coordinates
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f"{lat},{lng}",
        'radius': 50,  # Small radius to get closest place
        'key': settings.GOOGLE_MAPS_API_KEY
    }
    
    response = requests.get(url, params=params)
    places = response.json().get('results', [])
    
    if not places:
        return None
        
    # Get detailed information about the closest place
    place_id = places[0]['place_id']
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json"
    details_params = {
        'place_id': place_id,
        'fields': 'name,formatted_address,type,business_status',
        'key': settings.GOOGLE_MAPS_API_KEY
    }
    
    details_response = requests.get(details_url, params=details_params)
    return details_response.json().get('result')
def get_nearby_restaurants(lat, lng, radius=5000):
    """Get restaurants within specified radius"""
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f"{lat},{lng}",
        'radius': radius,
        'type': 'restaurant',
        'key': settings.GOOGLE_MAPS_API_KEY
    }
    
    response = requests.get(url, params=params)
    return response.json().get('results', [])