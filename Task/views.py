from functools import partial
from django.http.response import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from rest_framework.authtoken import serializers
from rest_framework.response import Response
from rest_framework import authentication, permissions,exceptions
from rest_framework.views import APIView
from rest_framework import mixins, generics
from django.utils.decorators import method_decorator

from CustomUser.models import Expert, UserProfile
from assignHelp.decorator import check_token

from .models import Task
from .serializers import TaskSerialzier 

@method_decorator(check_token, name='dispatch')
class TestList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerialzier

    def post(self,request,*args, **kwargs):
        data=request.data
        data['user']=self.kwargs['user'].id
        serializer=TaskSerialzier(data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("Success")
        else:
            return Response(serializer.errors,status=400)


@method_decorator(check_token, name='dispatch')
class GetUnassignedTask(generics.ListAPIView):
    def get(self,request,*args, **kwargs):
        expert_instance=get_object_or_404(Expert,user=self.kwargs['user'])
        queryset = Task.objects.filter(doer=expert_instance,status=1)

        return Response(TaskSerialzier(queryset,many=True).data)



@method_decorator(check_token, name='dispatch')
class Test(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerialzier
    lookup_fields = "pk"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        if obj.user==self.kwargs['user']:
            return obj
        else:
            raise exceptions.NotAcceptable("User not valid.")

    def post(self, request, *args, **kwargs):

        return self.partial_update(request, *args, **kwargs)

# @method_decorator(check_token, name='dispatch')
# class CreateTask(generics.CreateAPIView):
#     queryset=Task.objects.all()
#     serializer_class = TaskSerialzier

    
        

@method_decorator(check_token, name='dispatch')
class AssignTask(APIView):
    def post(self,request,*args, **kwargs):
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

@method_decorator(check_token, name='dispatch')
class UnassignedTask(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerialzier

    def get_queryset(self):
        return self.queryset.filter(doer=None)

@method_decorator(check_token, name='dispatch')
class AcceptTask(APIView):
    def post(self,request,*args, **kwargs):
        user=self.kwargs['user']
        taskID=request.data.get('taskID')
        task_query=Task.objects.filter(id=taskID)
        
        if task_query.exists():
            task_obj=task_query[0]
            if task_obj.doer.user==user:
                task_obj.status=3
                task_obj.save()
                return Response({"status":"success"})
            else:
                return Response({"status": 'Not allowed'})
        else:
            return HttpResponseBadRequest("Task doesn't exists.")

@method_decorator(check_token, name='dispatch')
class DeclineTask(APIView):
    def post(self,request,*args, **kwargs):
        taskID=request.data.get('taskID')

        task_query=Task.objects.filter(id=taskID)
        
        if task_query.exists():
            task_obj=task_query[0]
            if task_obj.doer==self.kwargs['user']:
                task_obj.status=1
                task_obj.save()
                return JsonResponse({"status":"declined"})
            return JsonResponse({"status":"declined"})
        else:
            return HttpResponseBadRequest("Task doesn't exists.")

@method_decorator(check_token, name='dispatch')
class ReviewTask(APIView):
    def post(self,request,*args, **kwargs):
        action=request.data.get('action')
        taskID=request.data.get('taskID')
        userID=self.kwargs['user'].id
        task_query=Task.objects.filter(id=taskID,user_id=userID)
        if task_query.exists():
            task_obj=task_query[0]
            if action=='1':
                task_obj.status=5
            if action=='2':
                task_obj.status=4
            if action is None:
                return HttpResponseBadRequest('Invalid Selection.')
        else:
            return HttpResponseNotFound('Task not found.')


