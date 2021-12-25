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
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user', on_delete=models.CASCADE, null=True)
    fname = models.CharField(max_length=24, null=True)
    lname = models.CharField(max_length=24, null=True)
    phone = models.IntegerField(null=True)
    avatar = models.ImageField(upload_to='avatar/',null=True)
    isStaff=models.BooleanField(default=False)
    referCode=models.TextField(null=True,unique=True)
    referedBy=models.TextField(null=True)
    referPoints=models.IntegerField(default=0)

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
    field=models.ManyToManyField(Fields)
    cv= models.FileField(upload_to='cv/')
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
