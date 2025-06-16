from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    courses = [
        {'title': 'Python для начинающих', 'description': 'Освойте основы Python за 4 недели'},
        {'title': 'Веб-разработка на Django', 'description': 'Создавайте мощные веб-приложения'},
        {'title': 'Алгоритмы и структуры данных', 'description': 'Подготовка к техническим собеседованиям'},
    ]
    context = {
        'title': 'BrainFunk - Онлайн курсы по программированию',
        'courses': courses,
        'promo_text': 'Обучаем программированию с 2023 года',
    }
    return render(request, 'main_page/index.html', context)

def about(request):
    return render(request, 'main_page/about.html', {'title': 'О нас'})

def contact(request):
    return render(request, 'main_page/contact.html', {'title': 'Контакты'})

def courses_catalog(request):
    return render(request, 'main_page/courses_catalog.html', {'title': 'Каталог курсов'})

@login_required
def profile(request):
    return render(request, 'main_page/profile.html')