# menu_pricing/urls.py
from django.urls import path
from menu_pricing import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-location-details/', views.get_location_details, name='get_location_details'),
]