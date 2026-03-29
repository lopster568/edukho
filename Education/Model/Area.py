from django.db import models


# Create your models here.





class Area(models.Model):
    Area_name = models.CharField(max_length=255, default="")
    State_id = models.CharField(max_length=250, default="")
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.CharField(max_length=250, default=1)
    def __str__(self):
        return self.Area_name