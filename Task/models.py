from typing import ForwardRef
from django.contrib.auth.models import User
from django.db import models
from django.db.models.expressions import Case
from django.template.defaultfilters import slugify
from CustomUser.models import UserProfile
from enum import Enum
from CustomUser.models import Expert
from mediaField.models import File, MediaFile

class Topic(models.Model):
    title=models.TextField(null=True,blank=True,unique=True)

    def __str__(self):
        return self.title


class statusChoice(Enum):
    unassigned=1
    working=2
    validating=3
    reforming=4
    completed=5

class Task(models.Model):
    user=models.ForeignKey(UserProfile,null=True,blank=True,on_delete=models.CASCADE)

    doer=models.ForeignKey(Expert,null=True,blank=True,on_delete=models.SET_NULL,related_name='task_doer')

    status=models.IntegerField(choices=((status.value,status.name) for status in statusChoice),default=1)

    title=models.TextField(null=True,blank=True)
    
    description=models.TextField(null=True,blank=True)
    completion_Date=models.DateField(null=True,blank=True)
    verified=models.BooleanField(default=False)
    attachment=models.FileField(upload_to='documents/',null=True,blank=True)
    active=models.BooleanField(default=False)

    def __str__(self):
        return self.title

    


