from django.shortcuts import render

# Create your views here.
def cart(request):
    return render(request, 'fourth_task/cart.html')

def games(request):
    title = "Games"
    name = "Игры"
    button = "Купить"
    games = Game.objects.all()
    context = {
        'title': title,
        'name': name,
        'button': button,
        'games': games,

    }
    return render(request, 'fourth_task/games.html', context)

def platform(request):
    return render(request, 'fourth_task/platform.html')

from sre_constants import error


from django.http import HttpResponse
from .forms import UserRegister
from .models import *

# Create your views here.

def sign_up_by_html(request):
    buyers = Buyer.objects.all()
    info = {}


    if request.method == "POST":
        # Получение данных:
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')

        # Обработка данных:

        if password == repeat_password and int(age) >= 18 and username not in buyers:
            Buyer.objects.create(name=username, balance=2000.0, age=age)
            return HttpResponse(f"Приветствуем, {username}!")
        elif password != repeat_password:
            info['error'] = 'Пароли не совпадают'
        elif int(age) < 18:
            info['error'] = 'Вы должны быть старше 18'
        elif username in buyers:
            info['error'] = 'Пользователь уже существует'

    return render(request, "fourth_task/registration_page.html", info)


def sign_up_by_django(request):
    users = ["Anton", "Andrey", "Maria", "Vasya"]
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)  # обращение request.POST не забыть
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            if username in users:
                info["error"] = "Пользователь уже существует"


            elif password != repeat_password:
                info["error"] = "Пароли не совпадают"


            elif age < "18":
                info["error"] = "Вы должны быть старше 18"

            elif username not in users and password == repeat_password and age >= "18":
                return HttpResponse(f"Приветствуем, {username}!")

            else:
                return render(request, "fourth_task/registration_page.html", info)


    else:
        info = {
            'form': UserRegister()
        }

    return render(request, "fourth_task/registration_page.html", info)