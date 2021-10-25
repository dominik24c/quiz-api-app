from quiz.models import Solution, Quiz
from rest_framework import serializers


class QuizSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Quiz
        fields = ('title', 'description', 'category')


class UserSolutionsListSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer()

    class Meta:
        model = Solution
        fields = ('id', 'quiz', 'created_at')

