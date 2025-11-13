from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum

class QuestionQuerySet(models.QuerySet):
    def with_answers_count(self):
        return self.annotate(answers_count=Count('answers'))

class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuerySet(self.model, using=self._db)
    
    def new_questions(self):
        return self.get_queryset().order_by('-created_date')
    
    def best_questions(self):
        return self.get_queryset().order_by('-rating')
    
    def by_tag(self, tag_name):
        return self.get_queryset().filter(tags__name=tag_name)

    def with_answers_count(self):
        return self.get_queryset().with_answers_count()

class ProfileManager(models.Manager):
    def best_profiles(self):
        return self.annotate(
            total_rating=Count('questions') + Count('answers')
        ).order_by('-total_rating')[:5]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    objects = ProfileManager()
    
    def __str__(self):
        return self.user.username

class TagManager(models.Manager):
    def popular_tags(self):
        return self.annotate(question_count=Count('question')).order_by('-question_count')[:10]

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    objects = TagManager()
    
    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag)
    created_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    
    objects = QuestionManager()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('app:question', kwargs={'question_id': self.id})

class AnswerManager(models.Manager):
    def for_question(self, question_id):
        return self.filter(question_id=question_id).order_by('-rating', '-created_date')

class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    
    objects = AnswerManager()
    
    def __str__(self):
        return f"Answer to {self.question.title}"

class QuestionLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='question_likes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_likes')
    value = models.SmallIntegerField()
    
    class Meta:
        unique_together = ['user', 'question']
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        total_rating = QuestionLike.objects.filter(question=self.question).aggregate(
            total=Sum('value')
        )['total'] or 0
        self.question.rating = total_rating
        self.question.save()

class AnswerLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_likes')
    value = models.SmallIntegerField()
    
    class Meta:
        unique_together = ['user', 'answer']
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        total_rating = AnswerLike.objects.filter(answer=self.answer).aggregate(
            total=Sum('value')
        )['total'] or 0
        self.answer.rating = total_rating
        self.answer.save()
