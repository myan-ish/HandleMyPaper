from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from rest_framework.authtoken import serializers
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework import mixins, generics

from CustomUser.models import UserProfile

from .models import Task
from .serializers import TaskSerialzier 

class TestList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerialzier

class Test(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerialzier
    lookup_fields = "pk"

class CreateTask(generics.CreateAPIView):
    queryset=Task.objects.all()
    serializer_class = TaskSerialzier


class AssignTask(APIView):
    def post(self,request):
        task=request.data.get('task')
        user=request.data.get('user')

        try:
            task_obj=Task.objects.get(id=task)
        except:
            raise ValueError('No task found.')

        try:
            task_obj.doer=UserProfile.objects.get(id=user)
        except:
            raise ValueError('No user found.')
        task_obj.status=2
        task_obj.save()

        return Response({'status':'success'})

class UnassignedTask(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerialzier

    def get_queryset(self):
        return self.queryset.filter(doer=None)

class AcceptTask(APIView):
    def post(self,request):
        userID=request.data.get('userID')
        taskID=request.data.get('taskID')

        task_query=Task.objects.filter(id=taskID)
        
        if task_query.exists():
            task_obj=task_query[0]
            task_obj.doer_id=taskID
            task_obj.status=3
            task_obj.save()
        else:
            raise HttpResponseBadRequest("Task doesn't exists.")

class DeclineTask(APIView):
    def post(self,request):
        userID=request.data.get('userID')
        taskID=request.data.get('taskID')

        task_query=Task.objects.filter(id=taskID)
        
        if task_query.exists():
            task_obj=task_query[0]
            task_obj.doer_id=taskID
            task_obj.status=1
            task_obj.save()
        else:
            raise HttpResponseBadRequest("Task doesn't exists.")

class ReviewTask(APIView):
    def post(self,request):
        action=request.data.get('action')
        taskID=request.data.get('taskID')
        userID=request.data.get('userID')
        task_query=Task.objects.filter(id=taskID,user_id=userID)
        if task_query.exists():
            task_obj=task_query[0]
            if action=='1':
                task_obj.status=5
            if action=='2':
                task_obj.status=4
            if action is None:
                raise HttpResponseBadRequest('Invalid Selection.')
        else:
            raise HttpResponseNotFound('Task not found.')


