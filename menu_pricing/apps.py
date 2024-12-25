# menu_pricing/apps.py
from django.apps import AppConfig
# menu_pricing/apps.py
from menu_pricing.utils.Logging_config import setup_logging


class MenuPricingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'menu_pricing'

    def ready(self):
        setup_logging()