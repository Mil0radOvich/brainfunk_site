from django.shortcuts import render

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