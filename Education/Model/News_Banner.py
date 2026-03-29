from django.db import models



class News_Banner(models.Model):
    state =  models.IntegerField()
    page = models.CharField(max_length=200,  default="")
    img = models.ImageField(upload_to='Education/News_Banner/', blank=True)
    banner_link_website = models.CharField(max_length=255, default="")
    cate = models.CharField(max_length=255, default="")
    title = models.CharField(max_length=255, default="")
    cate_home = models.CharField(max_length=255, default="")
    position=models.CharField(max_length=200,  default="")
    start_date = models.CharField(max_length=255, default="")
    end_date = models.CharField(max_length=255, default="")
    is_active = models.CharField(max_length=250, default=1)
    def __str__(self):
        return self.banner_link_website