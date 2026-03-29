from django.db import models

# Create your models here.

# 0 = "no", 1 = 'yes'
class HomepageMainBanner(models.Model):
    title = models.CharField(max_length=300, default="")
    banner_link_website = models.CharField(max_length=300, default="")
    img = models.ImageField(upload_to='Education/HomepageMainBanner/', blank=True)
    banner_position = models.CharField(max_length=255, default="")
    start_date = models.CharField(max_length=255, default="")
    end_date = models.CharField(max_length=255, default="")
    is_active = models.CharField(max_length=250, default=1)



    def __str__(self):
        return self.title