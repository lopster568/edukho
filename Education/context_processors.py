from .Model.Footer_section import Footer_Section

def common_footer_data(request):
    return {
        'footer_categories': Footer_Section.objects.all(),
    }
