from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': f'Question {i}',
            'id': i,
            'text': f'This is the text of question {i}',
            'tags': ['python', 'django'] if i % 2 == 0 else ['javascript', 'html'],
            'votes': i * 3,
            'answers': i % 5,
            'views': i * 10,
            'user': f'user{i}',
            'date': f'{i} hours ago'
        })
    
    page = paginate(questions, request, 5)
    return render(request, 'index.html', {
        'questions': page,
        'title': 'New Questions'
    })

def hot_questions(request):
    """Страница популярных вопросов"""
    questions = []
    for i in range(1, 25):
        questions.append({
            'title': f'Hot Question {i}',
            'id': i,
            'text': f'This is hot question {i}',
            'tags': ['popular', 'trending'],
            'votes': i * 10,
            'answers': i % 4,
            'views': i * 25,
            'user': f'hot_user{i}',
            'date': f'{i % 6} hours ago'
        })
    
    page = paginate(questions, request, 5)
    return render(request, 'index.html', {
        'questions': page,
        'title': 'Hot Questions'
    })

def questions_by_tag(request, tag_name):
    """Вопросы по определенному тегу"""
    questions = []
    for i in range(1, 20):
        questions.append({
            'title': f'Question about {tag_name} {i}',
            'id': i,
            'text': f'This question is related to {tag_name}',
            'tags': [tag_name, 'related'],
            'votes': i * 2,
            'answers': i % 3,
            'views': i * 8,
            'user': f'tag_user{i}',
            'date': f'{i % 4} hours ago'
        })
    
    page = paginate(questions, request, 5)
    return render(request, 'tag.html', {
        'questions': page,
        'tag_name': tag_name
    })

def question_page(request, question_id):
    """Страница одного вопроса с ответами"""
    question = {
        'title': f'Question {question_id}',
        'id': question_id,
        'text': f'Full text of question {question_id}. This is a detailed description of the problem.',
        'tags': ['python', 'django', 'web'],
        'votes': question_id * 5,
        'answers': 7,
        'views': question_id * 15,
        'user': 'author_user',
        'date': '5 hours ago'
    }
    
    answers = []
    for i in range(1, 12):
        answers.append({
            'id': i,
            'text': f'Answer {i} to question {question_id}. This is a detailed solution.',
            'votes': i * 3,
            'user': f'answer_user{i}',
            'date': f'{i} hours ago',
            'accepted': i == 1
        })
    
    page = paginate(answers, request, 5)
    return render(request, 'question.html', {
        'question': question,
        'answers': page
    })

def login_view(request):
    """Страница входа"""
    return render(request, 'login.html')

def signup_view(request):
    """Страница регистрации"""
    return render(request, 'signup.html')

def ask_view(request):
    """Страница создания вопроса"""
    return render(request, 'ask.html')

def settings_view(request):
    """Страница настроек пользователя"""
    user_data = {
        'username': 'ziontab',
        'email': 'ziontab@example.com',
        'reputation': 1256,
        'questions': 42,
        'answers': 87,
        'member_since': '2023'
    }
    return render(request, 'settings.html', {'user_data': user_data})

def logout_view(request):
    """Заглушка для выхода - перенаправляет на главную"""
    from django.shortcuts import redirect
    return redirect('app:index')