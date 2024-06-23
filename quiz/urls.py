from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, SubjectViewSet, UnitViewSet, TopicViewSet, QuestionViewSet, QuizSessionViewSet, AttemptViewSet, LeaderboardViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'units', UnitViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'quizsessions', QuizSessionViewSet)
router.register(r'attempts', AttemptViewSet)
router.register(r'leaderboard', LeaderboardViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
