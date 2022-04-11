from django.contrib.auth.models import Group, User
from django.db.models import fields, manager
from rest_framework import serializers
from .models import  Fields, Profile,UserProfile
from CustomUser import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username','password','email']
        # fields = '__all__'
    
    def getModel(self):
        return self.Meta.model.object.email

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Profile
        # fields = ['fname', 'lname','user', 'phone', 'coverPhoto','avatar','DOB','document','accountType']
        fields = '__all__'

    def create(self, validated_data):

        print(validated_data)
        user_data = validated_data.pop('user')
        
        # For Creating user manager is used
        user_obj = UserProfile.objects.create_user(**user_data)
        my_group,created = Group.objects.get_or_create(name='customer')
        my_group.user_set.add(user_obj)

        # for user_da in user_data:
        profile = Profile.objects.create(user=user_obj, **validated_data)

        return profile


class ProfileSeriL(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields= ['fname', 'lname', 'phone', 'avatar', 'referPoints','referCode']

class UserSer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=['id','username','email']

class FieldSer(serializers.ModelSerializer):
    class Meta:
        model=Fields
        fields='__all__'