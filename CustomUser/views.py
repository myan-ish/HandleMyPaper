from django import http
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.authtoken import serializers
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from django.core.mail.message import EmailMultiAlternatives
from rest_framework import authentication, permissions
from rest_framework import mixins, generics
from django.contrib.auth.models import User
from django.http import request
from django.http import response
from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse,
)
import datetime

from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.response import Response
from rest_framework import authentication, exceptions, permissions, serializers
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.parsers import JSONParser
from CustomUser.models import Expert, Fields, NewsLetter, Profile, UserProfile
from assignHelp.decorator import check_token
from .utils import generate_access_token, generate_refresh_token
from CustomUser.serializer import (
    FieldSer,
    ProfileSeriL,
    ProfileSerializer,
    UserSer,
    UserSerializer,
)


from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from assignHelp import settings
import jwt
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, mixins, serializers
import jwt
from jwt import exceptions as e


def decypher(token):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return data["user"]


def encrypt(payload):
    token = jwt.encode(payload, settings.SECRET_KEY)
    return token


def smtp(payload, email):
    token = encrypt({"user": payload})
    subject = "Welcome to Handle My Paper."
    message = (
        "Hello, "
        + " Please click on this link to activate your account: "
        + "http://127.0.0.1:8000/activate/?token="
        + str(token)
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
                        <a href="#"><img src="https://images.unsplash.com/photo-1604153138516-28db213cf26b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1115&q=80" alt="banner" style="height: 200px; width: 100%; object-fit: cover;"></a>
                        <div style="text-align: center; padding: 0 3rem;">
                            <h3>Thank you for registering</h3>
                            <p style="font-size: 0.75rem; margin-top: -0.5rem;">
                                We are happy to extend our greetings to you and we wish to continue working with you.
                                Visit our website and make yourself known as an expert for paid jobs by sending us an 
                                application or
                                submit your assignment to us and we will ensure to handle your assignment with care and
                                satisfy you to the fullest.
                            </p>
                            <a href="'''+ "http://127.0.0.1:8000/activate/?token="+ str(token)+'''"
                            <button style="padding: 0.5rem; border: none; background-color: #ab47bc; border-radius: 4px; color: white;">Get Started</button>
                        </div>
                    </td>
                </tr>
                <!-- Services -->
                <tr>
                    <td>
                        <table width="100%" style="border-spacing: 0;">
                            <tr>
                                <td class="columns">
                                    <!-- Expert -->
                                    <table class="column">
                                        <tr>
                                            <td class="padding">
                                                <table class="content">
                                                    <tr>
                                                        <td>
                                                            <a href="#"><img class="services" src="https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1172&q=80" alt="" width= "150" style="max-width: 150px; border-radius: 4px; object-fit: cover;"></a>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <h5>Be an Expert</h3>
                                                            <p style="font-size: 0.75rem;">Send us your C.V. to apply yourself as an expert and get tons of paid jobs that matches your specialization</p>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>

                                    <!-- Help -->
                                    <table class="column">
                                        <tr>
                                            <td class="padding">
                                                <table class="content">
                                                    <tr>
                                                        <td>
                                                            <a href="#"><img class="services" src="https://images.unsplash.com/photo-1509475826633-fed577a2c71b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1171&q=80" 
                                                            alt="" width= "150" style="max-width: 150px; border-radius: 4px; object-fit: cover;"></a>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <h5>Find an Expert</h3>
                                                            <p style="font-size: 0.75rem;">
                                                                If you are currently in need of an expert to handle your assignment, submit us your assignment and get your task handled by an expert with care.    
                                                            </p>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>

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

    recepient = email
    msg=EmailMultiAlternatives(subject,message,settings.EMAIL_HOST_USER,[recepient])
    msg.attach_alternative(html_content,"text/html")
    msg.send()


def token_validity(request):
    token = request.headers.get("token")
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return HttpResponse("Valid")
    except e.ExpiredSignatureError:
        return HttpResponseBadRequest("Token Expired, Please refetch access token")
    except e.InvalidSignatureError:
        return HttpResponseForbidden("Token Invalid")
    except e.DecodeError:
        return HttpResponseForbidden("Token Invalid")


@csrf_exempt
def activation(request):

    try:
        token_get = request.GET.get("token")

        decrypt = decypher(bytes(token_get, "utf-8"))
        user = UserProfile.objects.get(id=decrypt)
        if user:
            user.is_active = True
            user.save()
    except:
        return JsonResponse(status=400)
    return redirect("http://localhost:3000/login")


class Login(APIView):
    # queryset = UserSerializer.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        response = Response()

        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed("email and password required")

        user = UserProfile.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed("user not found")
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("wrong password")
        
        if not user.is_active :
            raise exceptions.AuthenticationFailed("Activate User.")

        serialized_user = UserSerializer(user).data
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
        response.data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return response


class Register(APIView):

    serializer_class = UserSerializer

    def post(self, request):
        data = JSONParser().parse(request)
        email = data["email"]
        data["user"] = {
            "username": data["username"],
            "email": data["email"],
            "password": data["password"],
        }
        try:
            userp = UserProfile.objects.get(email=data["email"])
        except:
            userp = None
        try:
            prof = Profile.objects.get(email=data["email"])
        except:
            prof = None

        if userp != None or prof != None:
            raise exceptions.NotAcceptable("Username or Email already in use.")

        serializer2 = ProfileSerializer(data=data)

        if serializer2.is_valid():

            serializer2.save()
            user = UserProfile.objects.get(email=email)
            smtp(user.pk, email)
            return Response({"User successfully created"})
        else:
            print(serializer2.errors)
            raise exceptions.ValidationError("User validation Error")


@method_decorator(check_token, name="dispatch")
class RegisterExpert(APIView):
    def post(self, request, *args, **kwargs):
        new_fields=[]
        fields = request.data.getlist("tags")
        print(fields)
        print(request.data)
        cv = request.data.get("cv")
        description=request.data.get("description")
        for _ in fields:
             new_fields=[Fields.objects.get_or_create(title=_)[0].id for _ in fields]
        
        expert_obj, created = Expert.objects.get_or_create(user=self.kwargs['user'])
        
        if not created:
            print("safas")
            raise exceptions.ValidationError("User is already expert.")
            

        expert_obj.cv = cv
        expert_obj.description = description
        expert_obj.field.set(new_fields)
        expert_obj.save()

        
        
        return HttpResponse("Success")


class UpdateProfile(generics.UpdateAPIView):
    # queryset = Profile.objects.all()
    # queryset = Item.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "id"

    def get_object(self):
        return Profile.objects.get(id=self.kwargs["id"])

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UpdateUserPw(APIView):
    def post(self, request, *args, **kwargs):
        currentPassword = request.data.get("currentPassword")
        newPw1 = request.data.get("newPassword")
        newPw2 = request.data.get("validatePassword")
        print(newPw1, newPw1)
        if newPw1 == newPw2:
            user_obj = UserProfile.objects.get(id=kwargs["id"])

            if user_obj.check_password(currentPassword):
                user_obj.set_password(newPw1)
                user_obj.save()
                return HttpResponse("Password Changed Successfully.")
            else:
                raise ValueError("Password Error, Please check again.")
        else:
            raise ValueError("Password Doesn't match.")


@method_decorator(check_token, name="dispatch")
class GetUser(APIView):
    def get(self, request, *args, **kwargs):
        response = Response()
        # print(request.user.id)
        print(self.kwargs["user"])
        response.data = {
            "profile": ProfileSeriL(Profile.objects.get(user=self.kwargs["user"])).data,
            "user": UserSer(self.kwargs["user"]).data,
            "isExpert":Expert.objects.filter(user=self.kwargs['user'], isExpert=True).exists(),

        }
        return response

@method_decorator(check_token, name="dispatch")
class GetFields(APIView):
    def get(self,request,*args, **kwargs):
        fields=Fields.objects.all()
        return Response(FieldSer(fields,many=True).data)

@method_decorator(check_token, name="dispatch")
class ReferPoint(APIView):
    def get(self,request,*args, **kwargs):
        referCode=self.kwargs['user'].referedBy
        referedUser=Profile.objects.filter(referCode=referCode).first()
        if referedUser:
            referedUser.referPoints+=5
            referedUser.save()
            return HttpResponse('Success')
        else:
            return HttpResponse('Not found')

@csrf_exempt
def smtpChangePw(payload, email):
    token = encrypt(
        {
            "user": payload,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            "iat": datetime.datetime.utcnow(),
        }
    )
    subject = "Request to change Password."
    message = (
        "You have requested to change your password , "
        + " Please click on this link to do so: "
        + "http://localhost:3000/reset/"
        + str(token)
    )
    print(message)
    recepient = email
    send_mail(
        subject, message, settings.EMAIL_HOST_USER, [recepient], fail_silently=False
    )

class IssuePassword(APIView):
    def post(self, request, *args, **kwargs):
        email=request.data['email']
        user = get_object_or_404(UserProfile,email=email)
        smtpChangePw(user.id, email)
        return HttpResponse('success')


class ForgotPassword(APIView):

    def post(self, request, token, *args, **kwargs):
        try:
            decrypt = decypher(bytes(token, "utf-8"))
            user_obj = UserProfile.objects.filter(id=decrypt).first()

            if user_obj is None:
                raise exceptions.AuthenticationFailed("User not found")

            user_obj.set_password(request.data.get("password"))
            user_obj.save()
            return HttpResponse("Success")

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed(
                {"message": "Refresh token error, please try again.", "statusCode": 106}
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                {
                    "message": "expired refresh token, please login again.",
                    "statusCode": 106,
                }
            )

# @method_decorator(check_token, name="dispatch")
class NewsLetterSubscription(APIView):
    def post(self,request,*args, **kwargs):
        email=request.data['email']
        news_letter_object,created=NewsLetter.objects.get_or_create(email=email)
        news_letter_object.is_subscribed=True
        news_letter_object.save()
        return HttpResponse('Success')

# @method_decorator(check_token, name="dispatch")
class NewsLetterUnSubscription(APIView):
    def get(self,request,*args, **kwargs):
        email=request.data['email']
        news_letter_object,created=NewsLetter.objects.get_or_create(email=request.data['email'])
        news_letter_object.is_subscribed=False
        news_letter_object.save()
        return HttpResponse('Success')
