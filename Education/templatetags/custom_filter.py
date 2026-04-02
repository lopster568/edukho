from django import template
import re

register = template.Library()

@register.filter(name='add_lists')
def add_lists(value, arg):
    """Custom filter to add two lists."""
    return value + arg

@register.filter(name='clean_embed_url')
def clean_embed_url(url):
    """Strip tracking params like ?si= from YouTube embed URLs."""
    if not url:
        return url
    return re.sub(r'[?&]si=[^&]*', '', url)

@register.filter(name='embed_to_watch_url')
def embed_to_watch_url(url):
    """Convert YouTube embed URL to a watchable URL."""
    if not url:
        return url
    url = re.sub(r'[?&]si=[^&]*', '', url)
    return url.replace('/embed/', '/watch?v=')

@register.filter(name='slugify_name')
def slugify_name(value):
    """Convert name to URL slug: 'Play School' -> 'play-school'"""
    if not value:
        return value
    return re.sub(r'[^a-z0-9]+', '-', str(value).lower()).strip('-')
