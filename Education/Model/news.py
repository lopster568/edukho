from django.db import models
from django.utils.text import slugify
import re

class News(models.Model):
    title      = models.CharField(max_length=200, default="")
    author     = models.CharField(max_length=200, default="")
    tags       = models.CharField(max_length=200, default="")
    category   = models.CharField(max_length=200, default="")
    desc       = models.TextField(default="")
    state      = models.CharField(max_length=200, default="")
    img        = models.ImageField(upload_to='Education/news/', blank=True)
    start_date = models.CharField(max_length=255, default="")
    end_date   = models.CharField(max_length=255, default="")
    is_active  = models.CharField(max_length=250, default=1)
    userid     = models.CharField(max_length=255, default="")

    # ✅ NEW FIELD
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # If two articles have same title, make slug unique e.g. my-title-2
            while News.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
