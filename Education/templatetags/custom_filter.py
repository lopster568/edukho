from django import template
import re

from Education.slug_utils import slugify_name as _slugify_name

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
    return _slugify_name(value)

@register.filter(name='banner_at')
def banner_at(banners, spec):
    """Return the first banner in `banners` matching `spec`, else None.

    spec is "<position>" or "<position>:home".
    - Matches News_Banner.position OR HomepageMainBanner.banner_position.
    - The ":home" suffix also requires cate_home == "1" (News right-column rule).
    Used to drive the paid-banner-wins / AdSense-fallback logic in templates.
    """
    if not banners:
        return None
    parts = str(spec).split(':')
    position = parts[0]
    require_home = len(parts) > 1 and parts[1] == 'home'
    for b in banners:
        val = getattr(b, 'position', None)
        if val is None:
            val = getattr(b, 'banner_position', None)
        if str(val) != position:
            continue
        if require_home and str(getattr(b, 'cate_home', '')) != '1':
            continue
        return b
    return None

@register.filter(name='format_tags')
def format_tags(value):
    """Normalize inconsistent tag separators to ' | '.

    'A |B latest | C' -> 'A | B latest | C'
    """
    if not value:
        return value
    parts = [p.strip() for p in value.split('|')]
    return ' | '.join(p for p in parts if p)


@register.filter(name='tags_to_keywords')
def tags_to_keywords(value):
    """Convert pipe-separated tags to a comma-separated meta keywords string.

    'Niti Ayog | Govt. Schools | Education News' -> 'Niti Ayog, Govt. Schools, Education News'
    """
    if not value:
        return value
    parts = [p.strip() for p in value.split('|')]
    return ', '.join(p for p in parts if p)
