from .Model.Footer_section import Footer_Section


def common_footer_data(request):
    links = Footer_Section.objects.filter(is_active="1").order_by('column_number', 'id')
    columns = {}
    for link in links:
        columns.setdefault(link.column_number, []).append(link)
    return {
        'footer_columns': columns,
    }
