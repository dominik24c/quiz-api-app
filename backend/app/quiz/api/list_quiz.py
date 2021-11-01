from django.db.models import Q, F
from quiz.models import Quiz
from quiz.serializers import QuizListSerializer
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class QuizListView(ListAPIView):
    serializer_class = QuizListSerializer

    # queryset = Quiz.objects.all()

    def get_queryset(self):
        searched_phrase = self.request.query_params.get('search')
        category = self.request.query_params.get('category')
        sort_by_date = self.request.query_params.get('sort_by_date')

        searched_phrase_filter = None
        category_filter = None
        date_filter = False
        if sort_by_date is not None:
            date_filter = sort_by_date

        if searched_phrase is not None:
            searched_phrase_filter = (Q(title__contains=searched_phrase) |
                                      Q(description__contains=searched_phrase))
        if category is not None:
            category_filter = (Q(category__name=category))

        if searched_phrase is not None and category is not None:
            quizzes = Quiz.objects.filter(searched_phrase_filter & category_filter)
        elif searched_phrase is not None:
            quizzes = Quiz.objects.filter(searched_phrase_filter)
        elif category_filter is not None:
            quizzes = Quiz.objects.filter(category_filter)
        else:
            quizzes = Quiz.objects.all()

        if date_filter:
            quizzes = quizzes.order_by(F('created_at').desc())
        else:
            quizzes = quizzes.order_by('created_at')

        return quizzes

    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response({
            'quizzes': serializer.data
        })
