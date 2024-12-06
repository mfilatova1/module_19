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

        if password != repeat_password:
            info['error'] = 'Пароли не совпадают'
        elif int(age) < 18:
            info['error'] = 'Вы должны быть старше 18'
        elif Buyer.objects.filter(name=username).exists():
            info['error'] = 'Пользователь уже существует'
        else:
            Buyer.objects.create(name=username, balance=2000.0, age=age)
            return HttpResponse(f"Приветствуем, {username}!")


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


from django.core.paginator import Paginator

#def game_list(request):
    # Получаем все игры
    #games = Game.objects.all()

    # if request.method == 'POST':
    #     if request.POST.get('page_len') == 'all':
    #         per_page = len(games)
    #         # Создаем пагинатор
    #         paginator = Paginator(games, per_page)
    #
    #         # Получаем текущую страницу из запроса
    #         page_number = request.GET.get('page', 1)
    #         page_obj = paginator.get_page(page_number)
    #
    #         return render(request, 'fourth_task/game_list.html', {'page_obj': page_obj})


class GamePage:
    # Количество игр на странице по умолчанию
    per_page = 3

    def game_list(self, request):
        # Получаем все игры из базы данных и сортируем их по цене
        games = Game.objects.all().order_by('-cost')

        # Проверяем, был ли запрос методом POST
        if request.method == 'POST':
            # Если пользователь хочет вывести все игры, устанавливаем per_page равным количеству всех игр
            if request.POST.get('page_len') == 'all':
                self.per_page = len(games)
            else:
                # Иначе устанавливаем количество игр на странице в зависимости от выбора пользователя
                self.per_page = int(request.POST.get('page_len'))

        # Создаем объект пагинатора с переданными играми и количеством игр на странице
        paginator = Paginator(games, self.per_page)

        # Пытаемся получить номер страницы из GET-запроса
        try:
            page_number = int(request.GET.get('page'))
        except TypeError:
            # Если не удалось получить номер страницы, устанавливаем его равным 1
            page_number = 1

        # Получаем нужную страницу с постами
        page_obj = paginator.get_page(page_number)

        # Список страниц для отображения в пагинаторе
        num_page_list = []

        # Проверяем, нужно ли добавлять '...' в список страниц (если впереди есть много страниц)
        if page_number - 2 > 1:
            num_page_list.append(0)

        # Добавляем номера страниц, которые будут отображаться
        for i in range(max(1, page_number - 2), min(paginator.num_pages, page_number + 2) + 1):
            num_page_list.append(i)

        # Проверяем, нужно ли добавлять '...' в список страниц (если позади есть много страниц)
        if page_number + 2 < paginator.num_pages:
            num_page_list.append(0)

        # Контекст, который будет передан в шаблон
        context = {
            'page_obj': page_obj,  # Объект с постами текущей страницы
            'paginator': paginator,  # Пагинатор с общей информацией
            'num_page_list': num_page_list  # Список номеров страниц для отображения
        }

        # Рендерим шаблон 'index.html' с переданным контекстом
        return render(request, 'fourth_task/game_list.html', context)


