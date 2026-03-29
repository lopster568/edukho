from django.db import models
from django.utils import timezone

class Event(models.Model):
    
    events = models.TextField(max_length=1000)
    event_image = models.ImageField(upload_to='Education/event',blank=True)
    event_date = models.DateTimeField(default=timezone.now)