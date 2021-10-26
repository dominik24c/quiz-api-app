import random

import factory
from django.contrib.auth.models import User
from django.db.models import QuerySet
from faker import Faker

from .models.answer import Answer
from .models.category import Category
from .models.question import Question
from .models.quiz import Quiz
from .models.solution import Solution

TEST_CATEGORIES = ['History', 'Mathematics', 'Music']
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.profile()['username']
    email = fake.profile()['mail']


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = random.choices(TEST_CATEGORIES)


class QuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quiz

    category = factory.SubFactory(CategoryFactory)
    owner = factory.SubFactory(UserFactory)
    title = "".join(fake.random_letters())
    description = fake.paragraph(nb_sentences=4)
    created_at = fake.date_time()


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    question = "".join(fake.random_letters())
    points, = fake.random_int(min=1, max=5),
    quiz = factory.SubFactory(QuizFactory)


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    question = factory.SubFactory(QuestionFactory)
    answer = "".join(fake.random_letters(length=5))
    is_correct = fake.pybool()


class SolutionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Solution

    quiz = factory.SubFactory(QuizFactory)
    solved_by = factory.SubFactory(UserFactory)

    @factory.post_generation
    def answers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for answer in extracted:
                self.answers.add(answer)


# class SolutionFactory(object):
#     @staticmethod
#     def create(quiz: Quiz, user: User, answers: QuerySet[Answer]) -> Solution:
#         solution = Solution.objects.create(
#             quiz=quiz,
#             solved_by=user,
#         )
#         for answer in answers:
#             solution.add(answer)
#         return solution
