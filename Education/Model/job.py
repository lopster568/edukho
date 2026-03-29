from django.db import models

# Create your models here.

class Job(models.Model):
    job_title = models.CharField(max_length=300, default="")
    job_category = models.CharField(max_length=300, default="")
    company = models.CharField(max_length=300, default="")
    state = models.CharField(max_length=300)
    job_desc = models.TextField(max_length=500, default="")
    experience = models.CharField(max_length=300, default="")
    pub_date = models.DateField(auto_now_add=True)
    salary = models.CharField(max_length=300, default="")
    end_date = models.DateField()
    is_active = models.CharField(max_length=250, default=1)
    userid = models.CharField(max_length=255, default="")
    def __str__(self):
        return self.job_title
