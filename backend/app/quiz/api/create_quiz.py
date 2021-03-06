from quiz.models import Quiz
from quiz.serializers import QuizSerializer

from rest_framework.generics import CreateAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


class QuizCreateView(RetrieveModelMixin, CreateAPIView):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Quiz was created!"
        })

    # def get(self, request: Request, *args, **kwargs) -> Response:
    #     serializer = self.get_serializer(self.get_queryset(), many=True)
    #     return Response({
    #         "quizzes": serializer.data
    #     })
