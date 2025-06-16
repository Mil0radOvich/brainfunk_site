import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brainfunk_site.settings')
django.setup()

from courses.models import *

def create_demo_content():
    User = get_user_model()
    
    # 1. Создаем преподавателя, если нет
    instructor, created = User.objects.get_or_create(
        username='demo_teacher',
        defaults={
            'email': 'teacher@example.com',
            'password': 'teacher123',
            'is_instructor': True
        }
    )
    
    # 2. Создаем категорию
    category, _ = Category.objects.get_or_create(
        name='Программирование',
        slug='programming'
    )
    
    # 3. Создаем курс с указанием преподавателя
    course, created = Course.objects.get_or_create(
        title="Python для начинающих",
        defaults={
            'slug': 'python-basics',
            'instructor': instructor,  # Указываем преподавателя
            'category': category,
            'description': 'Базовый курс по Python',
            'price': 9900,
            'duration': 40,
            'level': 'beginner'
        }
    )
    
    # 4. Создаем урок
    lesson, _ = Lesson.objects.get_or_create(
        course=course,
        title="Введение в Python",
        defaults={
            'order': 1,
            'duration': 45  # Длительность в минутах
        }
    )
    
    print("Демо-данные успешно созданы!")
    print(f"Курс: {course.title}")
    print(f"Преподаватель: {instructor.username}")
    print(f"Урок: {lesson.title}")

if __name__ == '__main__':
    create_demo_content()