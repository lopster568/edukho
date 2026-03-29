from django.db import models

class Search_Banner(models.Model):
    category = models.CharField(max_length=250, default="")
    state =  models.IntegerField(default=0)
    title = models.CharField(max_length=255, default="")
    area = models.IntegerField(default=0)
    page = models.CharField(max_length=200,  default="")
    img = models.ImageField(upload_to='Education/Search_Banner/', blank=True)
    banner_link_website = models.CharField(max_length=250, default="")
    position=models.CharField(max_length=200,  default="")
    start_date = models.CharField(max_length=255, default="")
    end_date = models.CharField(max_length=255, default="")
    is_active = models.CharField(max_length=250, default=1)

    def __str__(self):
        return self.banner_link_website