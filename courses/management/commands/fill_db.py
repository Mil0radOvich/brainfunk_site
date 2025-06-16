from django.core.management.base import BaseCommand
from courses.models import Course, Category
import random

class Command(BaseCommand):
    help = 'Fill database with test data'

    def handle(self, *args, **options):
        categories = ['Программирование', 'Дизайн', 'Маркетинг']
        for cat in categories:
            Category.objects.get_or_create(name=cat)
        
        for i in range(1, 21):
            Course.objects.create(
                title=f'Курс {i}',
                description=f'Описание курса {i}',
                price=random.randint(1000, 30000),
                duration=random.randint(5, 80)
            )