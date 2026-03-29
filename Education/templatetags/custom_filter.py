from django import template

register = template.Library()

@register.filter(name='add_lists')
def add_lists(value, arg):
    """Custom filter to add two lists."""
    return value + arg
