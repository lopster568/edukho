from django.db import models

# Create your models here.


class UserJobApply(models.Model):
    name = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default="")
    job_id = models.CharField(max_length=255, default="")
  

    def __str__(self):
        return self.name