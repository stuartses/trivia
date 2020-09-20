# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('session/', views.session, name='session'),
    path('trivia/<str:room_question>/', views.question, name='question'),
    path('end/<str:user_name>/', views.end, name='end'),
    path('defaultquestions/', views.default_questions, name='default_questions'),
    path('reset/', views.clear_games, name='clear_games'),
]
