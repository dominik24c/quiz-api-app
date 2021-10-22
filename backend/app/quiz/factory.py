import random
from typing import List

from django.contrib.auth.models import User

from .models.answer import Answer
from .models.category import Category
from .models.question import Question
from .models.quiz import Quiz

TEST_CATEGORIES = ['History', 'Mathematics', 'Music']


class CategoryFactory(object):
    @staticmethod
    def create(category_name: str) -> None:
        category_obj = Category.objects.create(name=category_name)
        category_obj.save()


class QuizFactory(object):
    @staticmethod
    def create(user: User) -> Quiz:
        category_name = random.choices(TEST_CATEGORIES)
        category = Category.objects.get(name=category_name[0])
        quiz = Quiz.objects.create(
            title='It is an example',
            description='Description text 1234',
            category=category,
            owner=user
        )
        quiz.save()
        return quiz
        # questions = Question()


class QuestionFactory(object):
    @staticmethod
    def create(quiz: Quiz) -> Question:
        question = Question.objects.create(
            question='question',
            points=3,
            quiz=quiz
        )
        question.save()
        return question


class AnswerFactory(object):
    @staticmethod
    def create(question: Question) -> Answer:
        answer = Answer.objects.create(
            question=question,
            answer='de2',
            is_correct=True
        )
        answer.save()
        return answer
