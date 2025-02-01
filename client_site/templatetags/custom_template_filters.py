from django.template import Library

register = Library()


@register.filter
def comma_separated(value):
    """Formats a number with commas as thousands separators."""
    try:
        return "{:,}".format(float(f'{value}'))
    except (ValueError, TypeError):
        return value

@register.filter
def subtract(value, num):
    """Subtract two numbers"""
    try:
        return value - num
    except (ValueError, TypeError):
        return value
