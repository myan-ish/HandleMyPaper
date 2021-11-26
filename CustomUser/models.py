from django.db import models
from django.contrib.auth import validators
from django.contrib.auth.models import AbstractUser

from . import manager as user_manager
from django.conf import settings


class Profile(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user', on_delete=models.CASCADE, null=True)
    fname = models.CharField(max_length=24, null=True)
    lname = models.CharField(max_length=24, null=True)
    phone = models.IntegerField(null=True)
    avatar = models.ImageField(upload_to='avatar/',null=True)
    isStaff=models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class UserProfile(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['email']
    objects = user_manager.UserProfileManager()

    def __str__(self):
        return self.username
