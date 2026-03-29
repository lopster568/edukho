# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.utils import timezone
# from .manager import CustomUserManager

# # member models here 

# class User_Member(AbstractBaseUser, PermissionsMixin):
#     password = models.CharField(max_length=200, default="")
#     i_am = models.CharField(max_length=250, default="")
#     name = models.CharField(max_length=300,  default="")
#     name_of_institution = models.CharField(max_length=200, default="")
#     address_of_institution =  models.CharField(max_length=200, default="")
#     country =  models.CharField(max_length=200, default="")
#     state =  models.CharField(max_length=200, default="")
    
#     contact_no =  models.CharField(max_length=200, default="")
#     user_email = models.CharField(max_length=200, default="")
#     user_web =  models.CharField(max_length=200, default="")
#     name_of_concerned_person =  models.CharField(max_length=200)
#     year_of_establishment =  models.CharField(max_length=200)
#     add_logo_of_instituion =  models.ImageField(upload_to='logo/')
#     salient_features =  models.TextField(max_length=1000, default="")
#     is_staff = models.BooleanField(default=True)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(default=timezone.now)
#     objects = CustomUserManager()
#     USERNAME_FIELD = 'user_email'
#     REQUIRED_FIELDS = []

    

#     def __str__(self):
#         return self.name

