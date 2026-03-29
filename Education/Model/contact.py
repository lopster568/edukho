from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=300, default="")
    email = models.EmailField(max_length=300, default="")
    msg = models.TextField(max_length=300, default="")
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.CharField(max_length=250, default=1)

    def __str__(self):
        return self.name
    