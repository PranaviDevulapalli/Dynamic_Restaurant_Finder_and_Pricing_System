from django.urls import path
from . import views

urlpatterns = [
    path('', views.pricing_view, name='pricing_view'),
]
