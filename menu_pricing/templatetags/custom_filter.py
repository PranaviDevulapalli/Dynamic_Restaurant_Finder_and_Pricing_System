# menu_pricing/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item_price(value):
    # Example logic to get item price
    return value.price
