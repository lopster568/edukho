from django.contrib import admin

# Register your models here.

from .Model.contact import Contact
from .Model.interview import Interview
from .Model.job import Job
from .Model.news import News
from .Model.HomepageMainBanner import HomepageMainBanner
from .Model.State import State
from .Model.Area import Area
from .Model.Search_Banner import Search_Banner
from .Model.News_Banner import News_Banner
from .Model.Job_banner import Job_Banner
from .Model.Interview_Banner import Interview_Banner

admin.site.register(Search_Banner)
admin.site.register(Contact)
admin.site.register(Interview)
admin.site.register(Job)
admin.site.register(News)
admin.site.register(HomepageMainBanner)
admin.site.register(State)
admin.site.register(Area)
admin.site.register(News_Banner)
admin.site.register(Job_Banner)
admin.site.register(Interview_Banner)