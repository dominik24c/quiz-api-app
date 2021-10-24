from django.db.models import ObjectDoesNotExist
from quiz.models import Solution, Answer, Quiz
from rest_framework import serializers


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id',)


class SolutionCreateSerializer(serializers.ModelSerializer):
    quiz_id = serializers.IntegerField(min_value=1)
    answers = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all(), many=True)

    quiz: Quiz

    class Meta:
        model = Solution
        fields = ('quiz_id', 'answers')

    # def validate(self, attrs):
        # quiz_id = attrs['quiz_id']
        # try:
        #     self.quiz = Quiz.objects.get(pk=quiz_id)
        # except ObjectDoesNotExist:
        #     raise serializers.ValidationError({
        #         "error": "Invalid quiz id passed! Quiz does not exist!!!"
        #     })

        # answers_data = Answer.objects.filter(question__quiz__pk=quiz_id)
        # # print(answers_data)
        # list_of_answers_pk = answers_data.values_list('id', flat=True)
        # # print(list_of_answers_pk)
        # keys_doesnt_belongs_to_quiz = []
        # for answer in attrs['answers']:
        #     if answer.pk not in list_of_answers_pk:
        #         keys_doesnt_belongs_to_quiz.append(answer.pk)
        #         # print(answer.pk)
        # if len(keys_doesnt_belongs_to_quiz) > 0:
        #     raise serializers.ValidationError({
        #         "error": "Invalid answers id passed! These answers doesn't belongs to this quiz!!!",
        #         "invalid-answers-keys": keys_doesnt_belongs_to_quiz
        #     })
        # return attrs

    def validate_quiz_id(self, value):
        try:
            self.quiz = Quiz.objects.get(pk=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({
                "error": "Invalid quiz id passed! Quiz does not exist!!!"
            })
        return value

    def create(self, validated_data) -> Solution:
        user = self.context['request'].user
        solution = Solution.objects.create(solved_by=user, quiz=self.quiz)
        answers = validated_data.pop('answers')

        for answer in answers:
            solution.answers.add(answer)

        return solution
