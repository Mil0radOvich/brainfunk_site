from django.contrib import admin
from .models import Category, Course, Review, Lesson
from .models import LessonContent, TextContent, VideoContent, CodeTask, Quiz, QuizQuestion, QuizOption

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Review)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    ordering = ('course', 'order')
    search_fields = ('title', 'content')

class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 1

class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1
    inlines = [QuizOptionInline]

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizQuestionInline]

admin.site.register(LessonContent)
admin.site.register(TextContent)
admin.site.register(VideoContent)
admin.site.register(CodeTask)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizQuestion)
admin.site.register(QuizOption)