import os
import django
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike
from faker import Faker
import random
from django.db import transaction

class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'
    
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент для генерации данных')
    
    def handle(self, *args, **options):
        ratio = options['ratio']
        fake = Faker('ru_RU')
        
        self.stdout.write(f'Начинаем заполнение базы данных с коэффициентом {ratio}')
        
        self.stdout.write('Очистка существующих данных...')
        QuestionLike.objects.all().delete()
        AnswerLike.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        users = []
        russian_names = [
            'иван', 'алексей', 'сергей', 'дмитрий', 'михаил', 'андрей', 'максим',
            'анна', 'елена', 'ольга', 'наталья', 'ирина', 'светлана', 'мария'
        ]
        
        for i in range(ratio):
            username = f'{random.choice(russian_names)}_{i}'
            try:
                user = User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    password='password123'
                )
                profile = user.profile
                users.append(profile)
                if i % 100 == 0 and i != 0:
                    self.stdout.write(f'Создано {i} пользователей')
            except Exception as e:
                self.stdout.write(f'Ошибка создания пользователя {username}: {e}')

        tags = []
        russian_tags = [
            'python', 'django', 'базы_данных', 'алгоритмы', 'html', 'css', 
            'javascript', 'linux', 'git', 'docker', 'машинное_обучение',
            'веб_разработка', 'мобильная_разработка', 'тестирование', 'sql'
        ]
        
        for tag_name in russian_tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        
        self.stdout.write(f'Создано {len(tags)} тегов')

        questions = []
        question_titles = [
            "Как настроить Django проект?",
            "В чем разница между списком и кортежем в Python?",
            "Как оптимизировать запросы к базе данных?",
            "Лучшие практики работы с Git",
            "Как работает асинхронность в Python?",
            "С чего начать изучение машинного обучения?",
            "Как развернуть приложение на сервере?",
            "В чем преимущества Docker?",
            "Как писать чистый код?",
            "Какие фреймворки выбрать для фронтенда?",
            "Как работает REST API?",
            "Что такое микросервисная архитектура?",
            "Как защитить веб-приложение?",
            "Оптимизация производительности сайта",
            "Мобильная разработка на React Native"
        ]
        
        for i in range(ratio * 10):
            author = random.choice(users)
            title = random.choice(question_titles) + f" ({i})"
            question = Question.objects.create(
                title=title,
                text=fake.text(max_nb_chars=500),
                author=author,
                rating=random.randint(-10, 100)
            )
            question_tags = random.sample(tags, min(3, len(tags)))
            question.tags.set(question_tags)
            questions.append(question)
            if i % 1000 == 0 and i!= 0:
                self.stdout.write(f'Создано {i} вопросов')
        
        answers = []
        for i in range(ratio * 100):
            author = random.choice(users)
            question = random.choice(questions)
            answer = Answer.objects.create(
                text=fake.text(max_nb_chars=300),
                author=author,
                question=question,
                is_correct=random.choice([True, False]) if i % 10 == 0 else False,
                rating=random.randint(-5, 50)
            )
            answers.append(answer)
            if i % 10000 == 0:
                self.stdout.write(f'Создано {i} ответов')

        question_likes_count = 0
        for i in range(ratio * 200):
            user = random.choice(users)
            question = random.choice(questions)
            try:
                QuestionLike.objects.create(
                    user=user,
                    question=question,
                    value=random.choice([-1, 1])
                )
                question_likes_count += 1
            except:
                pass
            if i % 20000 == 0:
                self.stdout.write(f'Создано {i} лайков вопросов')

        answer_likes_count = 0
        for i in range(ratio * 200):
            user = random.choice(users)
            answer = random.choice(answers)
            try:
                AnswerLike.objects.create(
                    user=user,
                    answer=answer,
                    value=random.choice([-1, 1])
                )
                answer_likes_count += 1
            except:
                pass
            if i % 20000 == 0 and i != 0:
                self.stdout.write(f'Создано {i} лайков ответов')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'База данных успешно заполнена:\n'
                f'Пользователей: {len(users)}\n'
                f'Тегов: {len(tags)}\n'
                f'Вопросов: {len(questions)}\n'
                f'Ответов: {len(answers)}\n'
                f'Лайков вопросов: {question_likes_count}\n'
                f'Лайков ответов: {answer_likes_count}'
            )
        )
