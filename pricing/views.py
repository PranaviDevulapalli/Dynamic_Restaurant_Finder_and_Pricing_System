# prices/views.py

from django.shortcuts import render
from menu_pricing.utils import calculate_dynamic_price, fetch_weather_data, fetch_google_places_busy_times


def pricing_view(request):
    """
    View for displaying the final dynamic prices for the restaurant's menu.
    """
    menu_items = {
        "Pasta": 12.0,
        "Pizza": 15.0,
        "Salad": 10.0,
    }
    village_location = "Hicksville, NY"

    try:
        # Fetch supporting data
        weather_data = fetch_weather_data(village_location)
        busy_times = fetch_google_places_busy_times(village_location)

        # Calculate final dynamic prices
        final_prices = {}
        for item, base_price in menu_items.items():
            final_prices[item] = calculate_dynamic_price(
                base_price=base_price,
                weather_data=weather_data,
                busy_times=busy_times
            )

    except Exception as e:
        print(f"Error: {e}")
        context = {
            'error': f"An error occurred: {e}"
        }
        return render(request, 'prices/error.html', context)

    context = {
        'menu_items': menu_items,
        'final_prices': final_prices,
        'weather_data': weather_data,
        'busy_times': busy_times,
    }

    return render(request, 'prices/pricing.html', context)
