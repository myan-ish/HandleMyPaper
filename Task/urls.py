from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken import views

from .views import AcceptTask, AssignTask, DeclineTask, GetUnassignedTask, ReviewTask, SendNewsletter, Test, TestList, UnassignedTask

urlpatterns = [
    path('task/<int:pk>/',Test.as_view()),
    path('task',TestList.as_view()),
    path('assign_task',AssignTask.as_view()),
    path('pending_accept',GetUnassignedTask.as_view()),
    path('unassigned_task',UnassignedTask.as_view()),
    path('accept_task',AcceptTask.as_view()),
    path('decline_task',DeclineTask.as_view()),
    path('review_task',ReviewTask.as_view()),
    path('send_news/',SendNewsletter.as_view()),

]