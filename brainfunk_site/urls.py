"""
URL configuration for brainfunk_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main_page import views as main_views
from courses.views import CourseListView, CourseDetailView, authors_view, partners_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Главная страница и базовые страницы
    path('', main_views.index, name='index'),
    path('about/', main_views.about, name='about'),
    path('contact/', main_views.contact, name='contact'),
    
    # Каталог курсов и связанные страницы
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/category/<slug:category_slug>/', CourseListView.as_view(), name='course_list_by_category'),
    path('courses/<slug:course_slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/authors/', authors_view, name='authors'),
    path('courses/partners/', partners_view, name='partners'),
]

