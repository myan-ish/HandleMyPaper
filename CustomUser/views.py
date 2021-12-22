from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.authtoken import serializers
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import mixins, generics
from django.contrib.auth.models import User
from django.http import request
from django.http import response
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.response import Response
from rest_framework import authentication, exceptions, permissions, serializers
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.parsers import JSONParser
from CustomUser.models import Profile, UserProfile
from assignHelp.decorator import check_token
from .utils import generate_access_token, generate_refresh_token
from CustomUser.serializer import ProfileSeriL, ProfileSerializer, UserSer, UserSerializer
from django.core.mail import send_mail
from assignHelp import settings
import jwt
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, mixins, serializers
import jwt
from jwt import exceptions as e


def decypher(token):
    data=jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return data['user']

def encrypt(payload):
    token=jwt.encode(payload,settings.SECRET_KEY)
    return token

def smtp(payload,email):
    token=encrypt({'user':payload})
    subject="Welcome to Sweed."
    message="Hello, "+" Please click on this link to activate your account: "+ 'http://127.0.0.1:8000/user/activate/?token='+str(token)
    recepient=email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient])

def token_validity(request):
    token = request.headers.get('token')
    try:
        data=jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return HttpResponse('Valid')
    except e.ExpiredSignatureError:
        return HttpResponseBadRequest('Token Expired, Please refetch access token')
    except e.InvalidSignatureError:
        return HttpResponseForbidden('Token Invalid')
    except e.DecodeError:
        return HttpResponseForbidden('Token Invalid')

@csrf_exempt
def activation(request):

    try:
        token_get=request.GET.get('token')
        
        decrypt=decypher(bytes(token_get,'utf-8'))
        user=UserProfile.objects.get(id=decrypt)
        if user:
            user.is_active=True
            user.save()
    except:
        return JsonResponse(status=400)
    return JsonResponse({'message':'Congrats, Your account is activaed.'})

class Login(APIView):
    # queryset = UserSerializer.objects.all()
    serializer_class = UserSerializer

    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        response=Response()

        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed(
            'email and password required')

        user = UserProfile.objects.filter(email=email).first()
        if(user is None):
            raise exceptions.AuthenticationFailed('user not found')
        if (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('wrong password')
    
        serialized_user = UserSerializer(user).data
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'refresh_token':refresh_token, 
        }

        return response

class Register(APIView):
    
    serializer_class = UserSerializer

    def post(self,request):
        data = JSONParser().parse(request)
        email=data['email']
        data['user']={'username': data['username'],'email': data['email'], 'password': data['password']}
        try:
            userp = UserProfile.objects.get(email=data['email'])
        except:
            userp=None
        try:
            prof = Profile.objects.get(email=data['email'])
        except:
            prof=None

        if userp !=None or  prof!=None:
            raise exceptions.NotAcceptable('Username or Email already in use.')

        serializer2= ProfileSerializer(data=data)

        if serializer2.is_valid():
           
            serializer2.save()
            user=UserProfile.objects.get(email=email)
            smtp(user.pk,email)
            return Response({'User successfully created'})
        else:
            print(serializer2.errors)
            raise exceptions.ValidationError('User validation Error')

class UpdateProfile(generics.UpdateAPIView):
    # queryset = Profile.objects.all()
    # queryset = Item.objects.all()
    serializer_class = ProfileSerializer
    lookup_field='id'

    def get_object(self):
        return Profile.objects.get(id=self.kwargs['id'])

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class UpdateUserPw(APIView):

    def post(self, request, *args, **kwargs):
        currentPassword=request.data.get('currentPassword')
        newPw1=request.data.get('newPassword')
        newPw2=request.data.get('validatePassword')
        print(newPw1,newPw1)
        if newPw1 == newPw2:
            user_obj=UserProfile.objects.get(id=kwargs['id'])

            if user_obj.check_password(currentPassword):
                user_obj.set_password(newPw1)
                user_obj.save()
                return HttpResponse('Password Changed Successfully.')
            else:
                raise ValueError('Password Error, Please check again.')
        else:
            raise ValueError("Password Doesn't match.")





class DeliveryLogin(APIView):
    serializer_class = UserSerializer

    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')

        response=Response()

        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed(
            'email and password required')

        group=UserProfile.objects.filter()
        user = UserProfile.objects.filter(email=email,groups__name='delivery').first()
        if(user is None):
            raise exceptions.AuthenticationFailed('user not found')
        if (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('wrong password')
    
        serialized_user = UserSerializer(user).data
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'refresh_token':refresh_token, 
        }

        return response

@method_decorator(check_token, name='dispatch')
class GetUser(APIView):
    def get(self,request,*args, **kwargs):
        response=Response()
        # print(request.user.id)
        response.data={
            'profile':ProfileSeriL(Profile.objects.get(user=self.kwargs['user'])).data,
            'user':UserSer(request.user).data
        }
        return response
        