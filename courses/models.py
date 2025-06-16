from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser

User = get_user_model()

class User(AbstractUser):
    is_instructor = models.BooleanField(
        'Преподаватель',
        default=False,
        help_text='Отметьте, если пользователь является преподавателем'
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='taught_courses',
        null=True,  # Разрешаем NULL временно
        blank=True  # Разрешаем пустое значение в формах
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration = models.PositiveIntegerField(help_text="Duration in hours")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    image = models.ImageField(
        upload_to='courses/',  # папка для сохранения
        blank=True,  # необязательное поле
        null=True   # может быть NULL в БД
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    students = models.ManyToManyField(User, through='Enrollment', related_name='enrolled_courses')
    
    @property
    def average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
    
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('completed', 'Завершенный'),
        ('canceled', 'Отмененный'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user} enrolled in {self.course}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"Review by {self.user} for {self.course}"

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField()
    photo = models.ImageField(upload_to='authors/')
    courses_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners/')
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.name
    
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    duration = models.PositiveIntegerField(
    help_text="Длительность в минутах",
    default=30  # Добавляем значение по умолчанию
    ) 
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.course.slug}-{self.title}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    


class LessonContent(models.Model):
    CONTENT_TYPES = [
        ('TEXT', 'Текстовый конспект'),
        ('VIDEO', 'Видео'),
        ('TASK', 'Практическое задание'),
        ('QUIZ', 'Тест')
    ]
    
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=5, choices=CONTENT_TYPES)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.get_content_type_display()} - {self.title}"

class TextContent(models.Model):
    content = models.OneToOneField(
        LessonContent,
        on_delete=models.CASCADE,
        related_name='text_content'
    )
    body = models.TextField()
    
    def __str__(self):
        return f"Текстовый блок: {self.content.title}"

class VideoContent(models.Model):
    content = models.OneToOneField(
        LessonContent,
        on_delete=models.CASCADE,
        related_name='video_content'
    )
    video_url = models.URLField()
    duration = models.PositiveIntegerField(help_text="Длительность в секундах")
    transcript = models.TextField(blank=True)
    
    def __str__(self):
        return f"Видео: {self.content.title}"

class CodeTask(models.Model):
    content = models.OneToOneField(
        LessonContent,
        on_delete=models.CASCADE,
        related_name='code_task'
    )
    description = models.TextField()
    starter_code = models.TextField(blank=True)
    solution = models.TextField()
    language = models.CharField(max_length=50, default='python')
    
    def __str__(self):
        return f"Задание: {self.content.title}"

class Quiz(models.Model):
    content = models.OneToOneField(
        LessonContent,
        on_delete=models.CASCADE,
        related_name='quiz'
    )
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"Тест: {self.content.title}"

class QuizQuestion(models.Model):
    QUESTION_TYPES = [
        ('MC', 'Множественный выбор'),
        ('CODE', 'Написание кода')
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=4, choices=QUESTION_TYPES)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Вопрос: {self.text[:50]}..."

class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='options')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Вариант: {self.text[:20]}"