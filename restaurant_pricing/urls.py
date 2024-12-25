# restaurant_pricing/urls.py (main project urls.py)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Include admin URLs if you're using Django admin
    path('', include('menu_pricing.urls')),  # Include the URLs from menu_pricing
]