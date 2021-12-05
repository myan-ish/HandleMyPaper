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
        try:
            if request.headers.get('token') is None:
                request = args[0]
            token=request.headers.get('token')
            data=jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            return HttpResponseBadRequest('Token Expired, Please refetch access token')
        except InvalidSignatureError:
            return HttpResponseForbidden('Token Invalid')
        except IndexError:
            return HttpResponseBadRequest('Token Required')

        try:
            current_user=UserProfile.objects.get(id=data['user_id'])
            login(request, current_user)
            return function(request, user=current_user, *args, **kwargs)
        except ModuleNotFoundError:
            return HttpResponseForbidden('Token Invalid')
    return wrap