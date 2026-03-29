from django.db import models

# Create your models here.


class Interview(models.Model):
    title = models.CharField(max_length=300, default="")
    name_of_person = models.CharField(max_length=300, default="")
    institution_name = models.CharField(max_length=300, default="")
    desc = models.TextField(max_length=1000, default="")
    profile = models.CharField(max_length=300, default="")
    instagram = models.CharField(max_length=300, default="")
    youtube = models.CharField(max_length=300, default="")
    twitter = models.CharField(max_length=300, default="")
    fb = models.CharField(max_length=300, default="")
    interview_name = models.CharField(max_length=300, default="")
    img = models.ImageField(upload_to='Education/interview/', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.CharField(max_length=250, default=1)

    def __str__(self):
        return self.title