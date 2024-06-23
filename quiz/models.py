from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='quiz_users',
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='quiz_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    is_paid = models.BooleanField(default=False)  # Add a field to indicate paid users
    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s subscription"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=100)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('1', 'Easy'),
        ('2', 'Medium'),
        ('3', 'Hard')
    ]

    TYPE_CHOICES = [
        ('mcq', 'Multiple Choice Question')
    ]

    unique_id = models.CharField(max_length=20, unique=True)
    text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    explanation = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class QuizSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)


class Attempt(models.Model):
    quiz_session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=200)
    is_correct = models.BooleanField()


class Leaderboard(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('all-time', 'All-time')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.name

class Bundle(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quizzes = models.ManyToManyField(Quiz)

    def __str__(self):
        return self.name

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True)
    bundle = models.ForeignKey(Bundle, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale {self.id} by {self.user.username}"



