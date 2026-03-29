from django.db import models


# Create your models here.





class Payment_table(models.Model):
    upi_no = models.CharField(max_length=255, default="")
    package_id = models.CharField(max_length=250, default="")
    slip_upload = models.ImageField(upload_to='Education/Payment/', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    userid = models.CharField(max_length=250, default="")
    is_active = models.CharField(max_length=250, default=0)
    def __str__(self):
        return self.upi_no