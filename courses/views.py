from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Course, Category, Author, Partner, Review
from django.db.models import Count, Avg

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('instructor', 'category')
        
        # Фильтрация по категории
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        
        # Фильтрация по уровню
        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # Сортировка
        sort = self.request.GET.get('sort')
        if sort == 'popular':
            queryset = queryset.annotate(
                students_count=Count('students')
            ).order_by('-students_count')
        elif sort == 'rating':
            queryset = queryset.annotate(
                avg_rating=Avg('reviews__rating')
            ).order_by('-avg_rating')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent__isnull=True)
        context['popular_courses'] = Course.objects.annotate(
            students_count=Count('students')
        ).order_by('-students_count')[:3]
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    slug_url_kwarg = 'course_slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        context['related_courses'] = Course.objects.filter(
            category=course.category
        ).exclude(pk=course.pk)[:4]
        context['reviews'] = course.reviews.select_related('user')[:5]
        return context

def authors_view(request):
    authors = Author.objects.all().order_by('-followers_count')
    return render(request, 'courses/authors.html', {'authors': authors})

def partners_view(request):
    partners = Partner.objects.all()
    return render(request, 'courses/partners.html', {'partners': partners})