from django.db import models

# Create your models here.



class Footer_Section(models.Model):
    user_id = models.CharField(max_length=255, default="")
    title = models.CharField(max_length=255, default="")
    footer_link = models.CharField(max_length=255, default="")
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.CharField(max_length=250, default=1)
    def __str__(self):
        return self.user_id
