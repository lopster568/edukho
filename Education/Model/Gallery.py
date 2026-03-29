# app/models.py

from django.db import models

class Gallery(models.Model):
    title = models.CharField(max_length=255)
    para = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)



class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery_images/')
