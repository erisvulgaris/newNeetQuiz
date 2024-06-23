from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, Subject, Unit, Topic, Question, QuizSession, Attempt, Leaderboard
from .serializers import CategorySerializer, SubjectSerializer, UnitSerializer, TopicSerializer, QuestionSerializer, QuizSessionSerializer, AttemptSerializer, LeaderboardSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return self.queryset.filter(category_id=category_id)
        return self.queryset

class UnitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def get_queryset(self):
        subject_id = self.request.query_params.get('subject_id')
        if subject_id:
            return self.queryset.filter(subject_id=subject_id)
        return self.queryset

class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_queryset(self):
        unit_id = self.request.query_params.get('unit_id')
        if unit_id:
            return self.queryset.filter(unit_id=unit_id)
        return self.queryset

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        topic_id = self.request.query_params.get('topic_id')
        difficulty = self.request.query_params.get('difficulty')
        type = self.request.query_params.get('type')
        queryset = self.queryset
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if type:
            queryset = queryset.filter(type=type)
        return queryset

class QuizSessionViewSet(viewsets.ModelViewSet):
    queryset = QuizSession.objects.all()
    serializer_class = QuizSessionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AttemptViewSet(viewsets.ModelViewSet):
    queryset = Attempt.objects.all()
    serializer_class = AttemptSerializer
    permission_classes = [IsAuthenticated]

class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

    def get_queryset(self):
        period = self.request.query_params.get('period')
        if period:
            return self.queryset.filter(period=period)
        return self.queryset