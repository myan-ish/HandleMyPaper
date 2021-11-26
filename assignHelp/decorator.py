from functools import wraps
from django import http
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
import jwt
from rest_framework.views import APIView
from CustomUser.models import UserProfile
from assignHelp import settings
from jwt.exceptions import *
from rest_framework import request

def check_token(function):
    @wraps(function)
    def wrap(request:request, *args, **kwargs):


        token=args[0].headers.get('token')
        request=args[0]
        try:
            data=jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            return HttpResponseBadRequest('Token Expired, Please refetch access token')
        except InvalidSignatureError:
            return HttpResponseForbidden('Token Invalid')
        # except DecodeError:
        #     return HttpResponseForbidden('Token Invalid')


        # print(data)
        # data=jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        try:
            current_user=UserProfile.objects.get(id=data['user_id'])
            login(request, current_user)
            return function(request, *args, **kwargs)

        except ModuleNotFoundError:
            return HttpResponseForbidden('Token Invalid')
    return wrap

# class check_token(APIView):

#     def get(request,*args, **kwargs):
#         token = request.headers.get('token')
#         print(request.headers)
#         print(args[0].get('token'))
#         print(token)
#         data=jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         print(data)
#         return

# def check_token(request):
#     token = request.headers.get('token')
#     print(token)
#     try:
#         data=jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#     except ExpiredSignatureError:
#         return HttpResponseBadRequest('Token Expired, Please refetch access token')
#     except InvalidSignatureError:
#         return HttpResponseForbidden('Token Invalid')

#     print(data)
#     # data=jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

#     try:
#         current_user=UserProfile.objects.get(id=data['user_id'])
#         login(request, current_user)
#         return HttpResponse('Allowed')

#     except ModuleNotFoundError:
#         return HttpResponseForbidden('Token Invalid')


