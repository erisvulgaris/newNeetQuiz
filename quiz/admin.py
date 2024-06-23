from django.contrib import admin
from .models import User, Category, Subject, Unit, Topic, Question, QuizSession, Attempt, Leaderboard, Chapter

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    search_fields = ('name', 'subject__name')
    list_filter = ('subject',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    search_fields = ('name', 'unit__name')
    list_filter = ('unit',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'text', 'topic', 'difficulty', 'type')
    search_fields = ('unique_id', 'text', 'topic__name')
    list_filter = ('difficulty', 'type', 'topic__unit__subject')

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'start_time', 'end_time')
    search_fields = ('user__username', 'topic__name')
    list_filter = ('start_time', 'end_time', 'topic__unit__subject')

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('quiz_session', 'question', 'selected_option', 'is_correct')
    search_fields = ('quiz_session__user__username', 'question__text')
    list_filter = ('is_correct', 'quiz_session__topic__unit__subject')

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'date', 'period')
    search_fields = ('user__username',)
    list_filter = ('period', 'date')

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    search_fields = ('name', 'subject__name')
    list_filter = ('subject',)