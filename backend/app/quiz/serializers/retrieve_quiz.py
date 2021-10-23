from quiz.models import Quiz
from rest_framework import serializers

from .create_quiz import QuestionSerializer


class QuizRetrieveSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='question_set')

    class Meta:
        model = Quiz
        fields = ('id', 'questions')
