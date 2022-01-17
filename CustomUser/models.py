from enum import Flag
from pyexpat import model
from django.db import models
from django.contrib.auth import validators
from django.contrib.auth.models import AbstractUser

from . import manager as user_manager
from django.conf import settings

import random,string

def random_key(length):
	key = ''
	for i in range(length):
		key += random.choice(string.hexdigits)
	return key

class Profile(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user', on_delete=models.CASCADE, null=True,blank=True)
    fname = models.CharField(max_length=24, null=True,blank=True)
    lname = models.CharField(max_length=24, null=True,blank=True)
    phone = models.IntegerField(null=True,blank=True)
    avatar = models.ImageField(upload_to='avatar/',null=True,blank=True)
    isStaff=models.BooleanField(default=False)
    referCode=models.TextField(null=True,unique=True,blank=True)
    referedBy=models.TextField(null=True,blank=True)
    referPoints=models.IntegerField(default=0,blank=True)

    def __str__(self):
        tempCode = random_key(6)
        while True:
            if Profile.objects.filter(referCode=tempCode).exists():
                tempCode = random_key(6)
            else:
                break
        self.referCode=tempCode

        return self.user.email

class Fields(models.Model):
    title=models.TextField(blank=True,null=True)

class Expert(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='expert_user', on_delete=models.CASCADE, null=True)
    field=models.TextField(null=True,blank=True)
    cv= models.FileField(upload_to='cv/',blank=True)
    isExpert=models.BooleanField(default=False)

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

class NewsLetter(models.Model):
    email=models.TextField(null=True,blank=True)
    is_subscribed=models.BooleanField(default=False)

    def __str__(self):
        return self.email+'-->' +str(self.is_subscribed)