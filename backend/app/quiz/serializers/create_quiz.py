from django.core.exceptions import ObjectDoesNotExist
from quiz.models import Quiz, Question, Answer, Category
from rest_framework import serializers

QUESTIONS_MIN_LENGTH = 3
ANSWERS_MIN_LENGTH = 2
QUESTIONS_MAX_LENGTH = 20
ANSWERS_MAX_LENGTH = 4


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('is_correct', 'id', 'answer')
        extra_kwargs = {
            "is_correct": {'write_only': True},
            "id": {'read_only': True}
        }


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, source='answer_set')

    class Meta:
        model = Question
        fields = ('id', 'question', 'points', 'answers')
        extra_kwargs = {
            "id": {'read_only': True}
        }

    def validate_answers(self, value):
        count = 0
        for answer in value:
            is_correct = answer['is_correct']
            if is_correct:
                count += 1

        if count == 0 and len(value) > 0:
            raise serializers.ValidationError({
                "error": f"You need at least one correct answer per question!!!",
            })

        if len(value) < ANSWERS_MIN_LENGTH:
            raise serializers.ValidationError({
                "error": f"You need at least {ANSWERS_MIN_LENGTH} "
                         f"answers for each question to create quiz!!!",
            })

        elif len(value) > ANSWERS_MAX_LENGTH:
            raise serializers.ValidationError({
                "error": f"You exceed the limit of answers for each question, you can "
                         f"have maximum {ANSWERS_MAX_LENGTH} answers per question."
            })

        return value

    def validate_question(self, value: str):
        if len(value) < 10:
            raise serializers.ValidationError({
                "error": "Question must have at least 10 characters!!!",
            })
        return value

    def validate_points(self, value: int):
        print(value)
        if not (0 < value < 6):
            raise serializers.ValidationError({
                "error": "The points must be between 1 to 5.",
            })
        return value


class QuizSerializer(serializers.ModelSerializer):
    category = serializers.CharField(min_length=3, max_length=100)
    questions = QuestionSerializer(many=True, source='question_set')
    category_obj: Category = None

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description', 'category', 'questions')
        extra_kwargs = {
            "id": {'read_only': True}
        }

    def validate_questions(self, value):
        if len(value) < QUESTIONS_MIN_LENGTH:
            raise serializers.ValidationError({"error": f"You need at least {QUESTIONS_MIN_LENGTH}"
                                                        f" questions to create quiz!!!"})
        elif len(value) > QUESTIONS_MAX_LENGTH:
            raise serializers.ValidationError({
                "error": f"You exceed the limit of questions per quiz, you can "
                         f"have maximum {QUESTIONS_MAX_LENGTH} questions per quiz. "
            })
        return value

    def validate_category(self, value):
        try:
            self.category_obj = Category.objects.get(name=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"error": "Category doesn't exists!"})
        return value

    def create(self, validated_data) -> Quiz:
        validated_data.pop('category')
        questions = validated_data.pop('question_set')

        user = self.context['request'].user

        quiz = Quiz.objects.create(owner=user, category=self.category_obj, **validated_data)

        for question in questions:
            answers = question.pop('answer_set')
            question_obj = Question.objects.create(quiz=quiz, **question)

            for answer in answers:
                Answer.objects.create(question=question_obj, **answer)

        return quiz
