from django.contrib.auth.models import User, Group
from django.db import models
from rest_framework import serializers

from Task.models import Task, statusChoice
from mediaField.models import MediaFile

# class GallerySerializer(serializers.ModelSerializer):
#     url=serializers.CharField(source='file.url')
#     class Meta:
#         model=MediaFile
#         fields='__all__'

# class TaskSerialzier(serializers.ModelSerializer):
#     gallery=GallerySerializer(data='gallery',many=True).initial_data
#     class Meta:
#         model = Task
#         fields = '__all__'


class TaskSerialzier(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = '__all__'
    
    def get_status(self,obj:Task):
        return statusChoice(obj.status).name