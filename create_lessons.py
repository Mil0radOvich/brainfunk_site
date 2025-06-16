import os
import django
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brainfunk_site.settings')
django.setup()

from courses.models import Course, Lesson

fake = Faker('ru_RU')

def create_lessons():
    courses = Course.objects.all()
    for course in courses:
        for i in range(1, 6):
            Lesson.objects.create(
                course=course,
                title=f"Урок {i}: {fake.sentence()}",
                content=fake.text(2000),
                duration=fake.random_int(min=5, max=60),
                order=i
            )
    print(f"Создано {Lesson.objects.count()} уроков")

if __name__ == '__main__':
    create_lessons()