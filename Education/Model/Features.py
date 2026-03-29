from django.db import models

# Create your models here.



class Features(models.Model):
    userid = models.CharField(max_length=255, default="")
    features = models.TextField(default="")
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.CharField(max_length=250, default=1)
    def __str__(self):
        return self.userid