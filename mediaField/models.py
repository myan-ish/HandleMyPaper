from django.db import models
from datetime import datetime

class File(models.Model):
    title=models.TextField(null=True,blank=True)
    file=models.FileField(null=True,blank=True,upload_to='attachment/')
    created_at=models.DateField(null=True,blank=True,auto_now=True)
    updated_at=models.DateField(null=True,blank=True)

    def save(self,*args, **kwargs):
        self.updated_at=datetime.now()
        return super().save(*args, **kwargs)

class MediaFile(models.Model):
    title=models.TextField(null=True,blank=True)
    file=models.FileField(null=True,blank=True,upload_to='media/')
    created_at=models.DateField(null=True,blank=True,auto_now=True)

    updated_at=models.DateField(null=True,blank=True)

    def save(self,*args, **kwargs):
        self.updated_at=datetime.now()
        return super().save(*args, **kwargs)