from rest_framework import serializers
from rest_framework.settings import api_settings


class QuizListSerializer(serializers.BaseSerializer):
    def to_representation(self, instance) -> list:
        response = []
        for quiz in instance:
            quiz_dict = {
                "id": quiz.id,
                "title": quiz.title,
                "description": quiz.description,
                "category": quiz.category.name,
                "owner": quiz.owner.username,
                "created_at": serializers.DateTimeField(api_settings.DATETIME_FORMAT).to_representation(
                    quiz.created_at),
                "num_of_questions": quiz.question_set.count(),
            }
            response.append(quiz_dict)
        return response
