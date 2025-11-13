from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from .models import Question, Tag, Profile

def paginate(objects_list, request, per_page=10):
    """Функция пагинации для всех списков"""
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page', 1)
    
    try:
        result_page = paginator.page(page)
    except PageNotAnInteger:
        result_page = paginator.page(1)
    except EmptyPage:
        result_page = paginator.page(paginator.num_pages)
        
    return result_page

def new_questions(request):
    """Главная страница - новые вопросы"""
    questions = Question.objects.new_questions().with_answers_count()
    page = paginate(questions, request, 20)
    
    popular_tags = Tag.objects.popular_tags()
    best_users = Profile.objects.best_profiles()
    
    return render(request, 'index.html', {
        'questions': page,
        'title': 'New Questions',
        'popular_tags': popular_tags,
        'best_users': best_users,
    })

def hot_questions(request):
    """Страница популярных вопросов"""
    questions = Question.objects.best_questions().with_answers_count()
    page = paginate(questions, request, 20)
    
    popular_tags = Tag.objects.popular_tags()
    best_users = Profile.objects.best_profiles()
    
    return render(request, 'index.html', {
        'questions': page,
        'title': 'Hot Questions',
        'popular_tags': popular_tags,
        'best_users': best_users,
    })

def questions_by_tag(request, tag_name):
    """Вопросы по определенному тегу"""
    questions = Question.objects.by_tag(tag_name).with_answers_count()
    page = paginate(questions, request, 20)
    
    popular_tags = Tag.objects.popular_tags()
    best_users = Profile.objects.best_profiles()
    
    return render(request, 'tag.html', {
        'questions': page,
        'tag_name': tag_name,
        'popular_tags': popular_tags,
        'best_users': best_users,
    })

def question_page(request, question_id):
    """Страница одного вопроса с ответами"""
    question = get_object_or_404(Question.objects.with_answers_count(), id=question_id)
    answers = question.answers.all()
    page = paginate(answers, request, 30)
    
    popular_tags = Tag.objects.popular_tags()
    best_users = Profile.objects.best_profiles()
    
    return render(request, 'question.html', {
        'question': question,
        'answers': page,
        'popular_tags': popular_tags,
        'best_users': best_users,
    })

def login_view(request):
    """Страница входа (заглушка)"""
    popular_tags = Tag.objects.popular_tags()
    best_users = Profile.objects.best_profiles()
    
    return render(request, 'login.html', {
        'popular_tags': popular_tags,
        'best_users': best_users,
    })

def signup_view(request):
    """Страница регистрации (заглушка)"""
    popular_tags = Tag.objects.popular_tags()
    best_users = Profile.objects.best_profiles()
    
    return render(request, 'signup.html', {
        'popular_tags': popular_tags,
        'best_users': best_users,
    })

def ask_view(request):
    """Страница создания вопроса (заглушка)"""
    popular_tags = Tag.objects.popular_tags()
    best_users = Profile.objects.best_profiles()
    
    return render(request, 'ask.html', {
        'popular_tags': popular_tags,
        'best_users': best_users,
    })

def settings_view(request):
    """Страница настроек пользователя (заглушка)"""
    popular_tags = Tag.objects.popular_tags()
    best_users = Profile.objects.best_profiles()
    
    user_data = {
        'username': 'GudAlex61',
        'email': 'gudalex61@example.com',
        'reputation': 1256,
        'questions': 42,
        'answers': 87,
        'member_since': '2023'
    }
    
    return render(request, 'settings.html', {
        'popular_tags': popular_tags,
        'best_users': best_users,
        'user_data': user_data,
    })

def logout_view(request):
    """Заглушка для выхода - перенаправляет на главную"""
    return HttpResponseRedirect(reverse('app:index'))
