from django.db import models

# Create your models here.

class Userpermission(models.Model):
    Salient_Features = models.CharField(max_length=255, default="")
    Job = models.CharField(max_length=255, default="")
    Event_Activity = models.CharField(max_length=255, default="")
    Video_Section = models.CharField(max_length=255, default="")
    About = models.CharField(max_length=255, default="")
    date = models.DateTimeField(auto_now_add=True)
    userid = models.CharField(max_length=250, default="")
    is_active = models.CharField(max_length=250, default=0)
    def __str__(self):
        return self.userid