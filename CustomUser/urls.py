from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken import views
from .utils import refresh_token_view

from CustomUser.views import ForgotPassword, GetFields, GetUser, IssuePassword, Login, NewsLetterSubscription, NewsLetterUnSubscription, Register, RegisterExpert, UpdateProfile, activation,UpdateUserPw, smtpChangePw, token_validity

urlpatterns = [
    path('obtain-token/', views.obtain_auth_token),
    path('validate_token/', token_validity),
    path('login/',Login.as_view()),
    path('getNewAccess/',refresh_token_view),
    path('register/',Register.as_view()),
    path('registerExpert/',RegisterExpert.as_view()),
    path('activate/', activation),
    path('updateProfile/<int:id>/', UpdateProfile.as_view()),
    path('updateUser/<int:id>/', UpdateUserPw.as_view()),
    path('get_user/',GetUser.as_view()),
    path('getField/',GetFields.as_view()),
    path('changePassword/<str:token>/', ForgotPassword.as_view()),
    path('issuePassword/', IssuePassword.as_view()),
    path('forgotmail/', smtpChangePw),
    path('subscribe/',NewsLetterSubscription.as_view()),
    path('unsubscribe/',NewsLetterUnSubscription.as_view())

]   