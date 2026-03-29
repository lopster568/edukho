from django.db import models


class Interview_Banner(models.Model):
    title = models.CharField(max_length=255, default="")
    page = models.CharField(max_length=200,  default="")
    img = models.ImageField(upload_to='Education/Interview_Banner/', blank=True)
    banner_link_website = models.CharField(max_length=300, default="")
    position=models.CharField(max_length=200,  default="")
    start_date = models.CharField(max_length=250, default="")
    end_date = models.CharField(max_length=250, default="")
    is_active = models.CharField(max_length=250, default=1)
    
    def __str__(self):
        return self.banner_link_website