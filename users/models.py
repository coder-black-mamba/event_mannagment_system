from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.


class CustomUser(AbstractUser): 
    phone_number = models.CharField( max_length=17, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_images', blank=True, null=True, default='profile_images/default.png')
    
    def __str__(self):
        return self.username