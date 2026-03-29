from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.apps import apps

def get_model(model_name):
    return apps.get_model('Education', model_name)

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'Education:homepage', 
            'Education:news', 
            'Education:job', 
            'Education:non_teaching',
            'Education:interview', 
            'Education:events',
            'Education:about',
            'Education:contact',
            'Education:advertising',
            'Education:work_with_us'
        ]

    def location(self, item):
        return reverse(item)

class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        News = get_model('News')
        # Added .order_by('-id') to fix the warning
        return News.objects.filter(is_active=1).order_by('-id')

    def location(self, obj):
        return reverse('Education:singlenews', args=[obj.id])

# ADD THIS: To include all your Interviews in the sitemap automatically
class InterviewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        Interview = get_model('Interview') # Ensure this matches your model name
        return Interview.objects.all().order_by('-id')

    def location(self, obj):
        return reverse('Education:single_interview', args=[obj.id])
