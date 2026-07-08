from .Model.Footer_section import Footer_Section
from .adsense_slots import ADSENSE_SLOTS


def common_footer_data(request):
    links = Footer_Section.objects.filter(is_active="1").order_by('column_number', 'id')
    columns = {}
    for link in links:
        columns.setdefault(link.column_number, []).append(link)
    return {
        'footer_columns': columns,
    }


def adsense_slots(request):
    """Expose AdSense ad-unit slot IDs to all templates as `adsense_slots`."""
    return {
        'adsense_slots': ADSENSE_SLOTS,
    }
