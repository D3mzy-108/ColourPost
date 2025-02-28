from django.template import Library

register = Library()


@register.filter
def comma_separated(value):
    """Formats a number with commas as thousands separators."""
    try:
        return "{:,}".format(float(f'{value}'))
    except:
        return value


@register.filter
def subtract(value, num):
    """Subtract two numbers"""
    try:
        return value - num
    except (ValueError, TypeError):
        return value


@register.filter
def percentage_ratio(value, num):
    """Calculate the percentage ratio between two values"""
    try:
        return (value/num) * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return value
