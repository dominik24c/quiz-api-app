from quiz.models import Quiz
from quiz.serializers import QuizRetrieveSerializer

from rest_framework.generics import RetrieveAPIView


class QuizRetrieveView(RetrieveAPIView):
    serializer_class = QuizRetrieveSerializer
    queryset = Quiz.objects.all()
