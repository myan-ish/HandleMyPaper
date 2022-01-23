from collections import OrderedDict
from functools import partial
from django.http.response import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from rest_framework.authtoken import serializers
from rest_framework.response import Response
from rest_framework import authentication, permissions,exceptions
from django.core.mail.message import EmailMultiAlternatives
from assignHelp import settings
from rest_framework.views import APIView
from rest_framework import mixins, generics
from django.utils.decorators import method_decorator

from CustomUser.models import Expert, NewsLetter, UserProfile
from assignHelp.decorator import check_token

from .models import Task
from .serializers import TaskSerialzier 
def smtp(email,message,news):
    subject = message
    message = (
        message
    )
    html_content='''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get Started</title>

    <style type="text/css">
        body {
            margin: 0;
            padding: 0;
            background-color: #EEEEEE;
        }
        table{
            border-spacing: 0;
        }
        td{
            padding: 0;
        }
        img {
            border: 0;
        }

        .wrapper {
            background-color: #EEEEEE;
            width: 100%;
            table-layout: fixed;
        }
        .webkit {
            max-width: 600px;
            padding-bottom: 1rem;
            background-color: #FFFFFF;
        }
        .outer {
            Margin: 0 auto;
            width: 100%;
            max-width: 600px;
            border-spacing: 0;
            font-family: 'Quicksand';
            color: #333333;
        }
        .columns{
            text-align: center;
            font-size: 0;
            line-height: 0;
            padding: 1.5rem 0;
        }
        .columns .column{
            width: 100%;
            max-width: 200px;
            display: inline-block;
            vertical-align: top;
        }
        .padding {
            padding: 0.75rem 1rem;
        }
        .columns .column .content{
            font-size: 1rem;
            line-height: 0.75rem;
        }

        @media screen and (max-width: 400px) {
            .services{
               width: 200px !important;
               height: 150px !important;
           }  
           .padding{
               padding-right: 0 !important;
               padding-left: 0 !important;
           }           
        }
    </style>
</head>

<body>
    <center class="wrapper">
        <div class="webkit">
            <table class="outer" style="margin: 0 auto">
                <!-- Header -->
                <tr>
                    <td>
                        <table width="100%" style="border-spacing: 0;">
                            <tr>
                                <td style="background-color: #FFFFFF; box-shadow: rgba(33, 35, 38, 0.1) 0px 10px 10px -10px; text-align: center;">
                                    <a href=""><img src="https://github.com/Nimesh-bot/HandleMyPaper/blob/main/HMP_logo.png?raw=true" alt="Logo" title="Logo" style="height: 5rem; width: 12rem; object-fit: contain;"></a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <!-- Body -->
                <tr>
                    <td>
                        <a href="#"><img src="https://images.unsplash.com/photo-1596526131083-e8c633c948d2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80" 
                            alt="banner" style="height: 200px; width: 100%; object-fit: cover;">
                        </a>
                        <div style="text-align: center; padding: 0 3rem;">
                            <h3>What's New?</h3>
                            <p style="font-size: 0.75rem; margin-top: -0.5rem;">
                                '''+news+'''
                            </p>

                        </div>
                    </td>
                </tr>
                <!-- Services -->

                <!-- Footer -->
                <tr>
                    <td>
                        <table width="100%" style="border-spacing: 0;">
                            <tr>
                                <td style="background-color: #FFFFFF; box-shadow: rgba(33, 35, 38, 0.1) 0px 10px 10px 10px; text-align: center;">
                                    <h5 style="color: #ab47bc;">Contact: <span style="color: #333333; font-weight: 100;">98XXXXXXXX</span></h5>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </div>
    </center>   
</body>
</html>
'''

    msg=EmailMultiAlternatives(subject,message,settings.EMAIL_HOST_USER,email)
    msg.attach_alternative(html_content,"text/html")
    msg.send()

@method_decorator(check_token, name='dispatch')
class TestList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerialzier

    def post(self,request,*args, **kwargs):
        data = OrderedDict()
        data.update(request.data)
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
            if task_obj.doer.user==self.kwargs['user']:
                task_obj.status=1
                task_obj.doer=None
                task_obj.save()
                return JsonResponse({"status":"declined"})
            return JsonResponse({"status":"user didn't match"})
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

# @method_decorator(check_token, name='dispatch')
class SendNewsletter(APIView):
    def post(self,request,*args, **kwargs):
        print(request.data)
        title=request.data['title']
        news=request.data['news']
        newletter_email=NewsLetter.objects.filter(is_subscribed=True).values("email")
        if newletter_email.exists():
            list_email = [ email['email'] for email in list(newletter_email) ]
            smtp(list_email,title,news)
        return HttpResponse(newletter_email)
