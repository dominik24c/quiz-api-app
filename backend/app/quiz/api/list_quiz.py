from quiz.models import Quiz
from quiz.serializers import QuizListSerializer
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class QuizListView(ListAPIView):
    serializer_class = QuizListSerializer
    queryset = Quiz.objects.all()

    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response({
            'quizzes': serializer.data
        })
