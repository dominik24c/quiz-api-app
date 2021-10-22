# Create your tests here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .factory import CategoryFactory, AnswerFactory, QuizFactory, QuestionFactory, TEST_CATEGORIES


class BaseApiTestCase(APITestCase):
    def setUp(self) -> None:
        user = User(username='test_user', email='test@gmail.com')
        user.set_password('test1234')
        user.save()

    def _test_get(self, namespace: str, status: str) -> Response:
        url = reverse(namespace)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status)

        return response

    def _test_post(self, namespace: str, status: str, data: dict) -> Response:
        url = reverse(namespace)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status)
        return response


class CategoryApiTest(BaseApiTestCase):
    def test_get_list_of_categories(self) -> None:
        [CategoryFactory.create(category_name) for category_name in TEST_CATEGORIES]

        self._test_get('quiz:list-category', status.HTTP_401_UNAUTHORIZED)

        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user)

        response = self._test_get('quiz:list-category', status.HTTP_200_OK)

        self.assertCountEqual(response.data['categories'], TEST_CATEGORIES)
        self.assertListEqual(response.data['categories'], TEST_CATEGORIES)


class QuizApiTest(BaseApiTestCase):
    def test_list_quiz(self) -> None:
        [CategoryFactory.create(category_name) for category_name in TEST_CATEGORIES]
        user = User.objects.get(username='test_user')
        quiz = QuizFactory.create(user)
        question = QuestionFactory.create(quiz)
        AnswerFactory.create(question)
        AnswerFactory.create(question)

        self._test_get('quiz:create-list-quiz', status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=user)

        response = self._test_get('quiz:create-list-quiz', status.HTTP_200_OK)
        quizzes = response.data['quizzes']
        self.assertEqual(len(quizzes), 1)

    def test_create_quiz(self) -> None:
        CategoryFactory.create('Mathematics')

        data = {
            "title": "Basic knowledge",
            "description": "This is quiz about the knowledge of the primary mathematics",
            "category": "Mathematics",
            "questions": [
                {
                    "question": "how many sides does the triangle have",
                    "points": 1,
                    "answers": [
                        {
                            "answer": "1",
                            "is_correct": False
                        },
                        {
                            "answer": "2",
                            "is_correct": False
                        },
                        {
                            "answer": "3",
                            "is_correct": True
                        }
                    ]
                },
                {
                    "question": "Solve equation 3+2*4=?",
                    "points": 2,
                    "answers": [
                        {
                            "answer": "20",
                            "is_correct": False
                        },
                        {
                            "answer": "11",
                            "is_correct": True
                        },
                        {
                            "answer": "14",
                            "is_correct": False
                        }
                    ]
                },
                {
                    "question": "The sum of the internal angles of the triangles equals:",
                    "points": 3,
                    "answers": [
                        {
                            "answer": "90",
                            "is_correct": False
                        },
                        {
                            "answer": "180",
                            "is_correct": True
                        },
                        {
                            "answer": "270",
                            "is_correct": False
                        }
                    ]
                }
            ]
        }

        self._test_post('quiz:create-list-quiz', status.HTTP_401_UNAUTHORIZED, data)

        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user)

        response = self._test_post('quiz:create-list-quiz', status.HTTP_200_OK, data)
        self.assertEqual(response.data['message'], 'Quiz was created!')
        # data['description'] = ''
        #
        # print(response.data)
