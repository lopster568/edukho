from django.db import models

class Banners(models.Model):
    home_banner = models.ImageField(upload_to='Education/Banners/home', blank=True)
    