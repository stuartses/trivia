# chat/views.py
from django.shortcuts import render
from django.http import HttpResponse
from chat import questions
from .models import Players, Games
import json


def index(request):
    return render(request, 'chat/index.html')


def signin(request):
    return render(request, 'chat/signin.html')


def register(request):
    new_user = Players()
    new_user.name = request.POST.get('user')
    new_user.email = request.POST.get('email')
    new_user.save()

    return render(request, 'chat/register.html', {'user': new_user.name})


def login(request):
    return render(request, 'chat/login.html')


def session(request):
    user_name = request.POST.get('user')
    email = request.POST.get('email')
    context = {}
    context['user'] = ""

    if Players.objects.filter(name=user_name).exists():
        user_obj = Players.objects.filter(name=user_name)[0]
        if (user_obj.email == email):
            context['user'] = user_name

    return render(request, 'chat/session.html', context)


def question(request, room_question):
    questions_list = questions.load(room_question)

    next_room = ""
    last_question = 0

    if (room_question == 'question1'):
        next_room = "question2"
    if (room_question == 'question2'):
        next_room = "question3"
    if (room_question == 'question3'):
        next_room = "end"
        last_question = 1

    context = {
        'room_name': room_question,
        'question_data': questions_list,
        'next_room': next_room,
        'last_question': last_question
    }

    return render(request, 'chat/questions.html', context)


def end(request):
    all_games = Games.objects.all()
    users = {}

    for game in all_games:
        game_inst = json.loads(game.instance)

        for user in game_inst:
            user_data = game_inst[user]
            user_name = user_data['user']

            if user_name in users:
                users[user_name] += user_data['score']
            else:
                users[user_name] = user_data['score']

    return render(request, 'chat/end.html', context={'scores': users})

# insert default questions to data base from http request


def default_questions(request):
    questions.default_data()

    return HttpResponse('Default questions in database')


def clear_games(request):
    all_games = Games.objects.all()

    for game in all_games:
        id = game.id
        game_obj = Games.objects.get(id=id)
        game_obj.instance = '{}'
        game_obj.save()

    return HttpResponse('Game reset')
