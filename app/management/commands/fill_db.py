import os
import django
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike
from faker import Faker
import random
from django.db import transaction
from django.db.models import Max

class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'
    
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент для генерации данных')
    
    def handle(self, *args, **options):
        ratio = options['ratio']
        
        self.stdout.write(f'Начинаем заполнение базы данных с коэффициентом {ratio}')
        self.stdout.write('Очистка существующих данных...')
        AnswerLike.objects.all().delete()
        QuestionLike.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        russian_names = [
            'иван', 'алексей', 'сергей', 'дмитрий', 'михаил', 'андрей', 'максим',
            'анна', 'елена', 'ольга', 'наталья', 'ирина', 'светлана', 'мария'
        ]
        
        domains = ['gmail.com', 'yandex.ru', 'mail.ru', 'hotmail.com']
        
        question_templates = [
            "Как настроить {}?",
            "В чем разница между {} и {}?",
            "Как оптимизировать {}?",
            "Лучшие практики работы с {}",
            "Как работает {}?",
            "С чего начать изучение {}?",
            "Как развернуть {} на сервере?",
            "В чем преимущества {}?",
            "Как писать {}?",
            "Какие {} выбрать для {}?",
            "Как работает {}?",
            "Что такое {}?",
            "Как защитить {}?",
            "Оптимизация {}",
            "Разработка на {}"
        ]
        
        tech_terms = [
            'python', 'django', 'базы данных', 'алгоритмы', 'html', 'css', 
            'javascript', 'linux', 'git', 'docker', 'машинное обучение',
            'веб разработка', 'мобильная разработка', 'тестирование', 'sql',
            'postgresql', 'redis', 'nginx', 'react', 'vue', 'angular',
            'rest api', 'graphql', 'микросервисы', 'kubernetes', 'aws',
            'цифровая безопасность', 'нейронные сети', 'блокчейн', 'big data'
        ]
        
        answer_templates = [
            "Для решения этой проблемы нужно {}.",
            "Я рекомендую использовать {}.",
            "Лучший подход - это {}.",
            "В данном случае поможет {}.",
            "Основные шаги: {}.",
            "Сначала нужно {}, затем {}.",
            "Это зависит от {}, но обычно {}.",
            "Я сталкивался с подобным и решил через {}.",
            "По моему опыту, лучше всего {}.",
            "Можно использовать {} или {}."
        ]

        self.stdout.write('Создание пользователей...')
        users = []
        profiles = []

        user_objs = []
        for i in range(ratio):
            name = random.choice(russian_names)
            username = f'{name}_{i}'
            email = f'{name}{i}@{random.choice(domains)}'
            user = User(
                username=username,
                email=email,
                password='password123'
            )
            user_objs.append(user)

            if i % 5000 == 0 and i > 0:
                self.stdout.write(f'Подготовлено {i} пользователей')

        User.objects.bulk_create(user_objs)
        self.stdout.write(f'Создано {len(user_objs)} пользователей')

        created_users = User.objects.filter(username__startswith=f'{russian_names[0]}_')
        profile_objs = []
        for user in created_users:
            profile = Profile(user=user)
            profile_objs.append(profile)
        
        Profile.objects.bulk_create(profile_objs)
        self.stdout.write(f'Создано {len(profile_objs)} профилей')

        profiles = list(Profile.objects.all())

        self.stdout.write('Создание тегов...')
        tag_objs = []
        for i in range(ratio):
            if i < len(tech_terms):
                tag_name = tech_terms[i]
            else:
                tag_name = f'технология_{i}'
            
            tag = Tag(name=tag_name)
            tag_objs.append(tag)
        
        Tag.objects.bulk_create(tag_objs)
        tags = list(Tag.objects.all())
        self.stdout.write(f'Создано {len(tags)} тегов')

        self.stdout.write('Создание вопросов...')
        question_objs = []
        for i in range(ratio * 10):
            author = random.choice(profiles)

            template = random.choice(question_templates)
            if template.count('{}') == 1:
                title = template.format(random.choice(tech_terms))
            elif template.count('{}') == 2:
                title = template.format(random.choice(tech_terms), random.choice(tech_terms))
            else:
                title = f"Вопрос о {random.choice(tech_terms)}"

            text_parts = []
            for _ in range(random.randint(2, 5)):
                answer_template = random.choice(answer_templates)
                if answer_template.count('{}') == 1:
                    text_parts.append(answer_template.format(random.choice(tech_terms)))
                elif answer_template.count('{}') == 2:
                    text_parts.append(answer_template.format(random.choice(tech_terms), random.choice(tech_terms)))
                else:
                    text_parts.append(f"Рассмотрим аспект {random.choice(tech_terms)}.")
            
            text = ' '.join(text_parts)
            
            question = Question(
                title=title + f" ({i})",
                text=text,
                author=author,
                rating=random.randint(-10, 100),
                created_date=django.utils.timezone.now()
            )
            question_objs.append(question)
            
            if i % 10000 == 0 and i > 0:
                self.stdout.write(f'Подготовлено {i} вопросов')
        
        Question.objects.bulk_create(question_objs)
        questions = list(Question.objects.all())
        self.stdout.write(f'Создано {len(questions)} вопросов')

        self.stdout.write('Добавление тегов к вопросам...')
        for i, question in enumerate(questions):
            question_tags = random.sample(tags, min(1, len(tags)))
            question.tags.set(question_tags)
            
            if i % 10000 == 0 and i > 0:
                self.stdout.write(f'Добавлены теги к {i} вопросам')

        self.stdout.write('Создание ответов...')
        answer_objs = []
        for i in range(ratio * 100):
            author = random.choice(profiles)
            question = random.choice(questions)

            answer_template = random.choice(answer_templates)
            if answer_template.count('{}') == 1:
                text = answer_template.format(random.choice(tech_terms))
            elif answer_template.count('{}') == 2:
                text = answer_template.format(random.choice(tech_terms), random.choice(tech_terms))
            else:
                text = f"Решение включает использование {random.choice(tech_terms)}."
            
            answer = Answer(
                text=text,
                author=author,
                question=question,
                is_correct=random.random() < 0.1,
                rating=random.randint(-5, 50),
                created_date=django.utils.timezone.now()
            )
            answer_objs.append(answer)
            
            if i % 100000 == 0 and i > 0:
                self.stdout.write(f'Подготовлено {i} ответов')
        
        Answer.objects.bulk_create(answer_objs)
        answers = list(Answer.objects.all())
        self.stdout.write(f'Создано {len(answers)} ответов')

        self.stdout.write('Создание лайков вопросов...')
        question_like_objs = []
        existing_likes = set()
        
        for i in range(ratio * 100):
            user = random.choice(profiles)
            question = random.choice(questions)

            like_key = (user.id, question.id)
            if like_key in existing_likes:
                continue
                
            existing_likes.add(like_key)
            
            question_like = QuestionLike(
                user=user,
                question=question,
                value=random.choice([-1, 1])
            )
            question_like_objs.append(question_like)
            
            if i % 50000 == 0 and i > 0:
                self.stdout.write(f'Подготовлено {i} лайков вопросов')
        
        QuestionLike.objects.bulk_create(question_like_objs)
        self.stdout.write(f'Создано {len(question_like_objs)} лайков вопросов')

        self.stdout.write('Создание лайков ответов...')
        answer_like_objs = []
        existing_answer_likes = set()
        
        for i in range(ratio * 100):
            user = random.choice(profiles)
            answer = random.choice(answers)
            
            like_key = (user.id, answer.id)
            if like_key in existing_answer_likes:
                continue
                
            existing_answer_likes.add(like_key)
            
            answer_like = AnswerLike(
                user=user,
                answer=answer,
                value=random.choice([-1, 1])
            )
            answer_like_objs.append(answer_like)
            
            if i % 50000 == 0 and i > 0:
                self.stdout.write(f'Подготовлено {i} лайков ответов')
        
        AnswerLike.objects.bulk_create(answer_like_objs)
        self.stdout.write(f'Создано {len(answer_like_objs)} лайков ответов')

        self.stdout.write(
            self.style.SUCCESS(
                f'База данных успешно заполнена:\n'
                f'Пользователей: {len(profiles)}\n'
                f'Тегов: {len(tags)}\n'
                f'Вопросов: {len(questions)}\n'
                f'Ответов: {len(answers)}\n'
                f'Лайков вопросов: {len(question_like_objs)}\n'
                f'Лайков ответов: {len(answer_like_objs)}\n'
                f'Всего оценок: {len(question_like_objs) + len(answer_like_objs)}'
            )
        )
