# Create your tests here.
import copy

from django.contrib.auth.models import User
from quiz.models import Category, Quiz, Answer
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .factories import CategoryFactory, AnswerFactory, QuizFactory, QuestionFactory, UserFactory, SolutionFactory, \
    TEST_CATEGORIES
from .test_data_dict import DATA


def create_test_data(number_of_quizzes=1) -> None:
    user = User.objects.get(username='test_user')
    category = Category.objects.get(name='Mathematics')

    for _ in range(number_of_quizzes):
        quiz = QuizFactory.create(owner=user, category=category, title='It is an example')
        question = QuestionFactory(quiz=quiz)
        AnswerFactory(question=question, is_correct=True)
        AnswerFactory(question=question, is_correct=False)


class BaseAuthApiTestCase(APITestCase):
    def _test_get(self, namespace: str, status: str, kwargs=None) -> Response:
        if kwargs is None:
            kwargs = {}
        url = reverse(namespace, kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status)

        return response

    def _test_post(self, namespace: str, status: str, data: dict) -> Response:
        url = reverse(namespace)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status)
        return response


class BaseApiTestCase(BaseAuthApiTestCase):
    TITLE = 'title'
    DESC = 'description'
    QUESTIONS = 'questions'
    QUESTION = 'question'
    CATEGORY = 'category'
    POINTS = 'points'
    ANSWERS = 'answers'
    ANSWER = 'answer'
    IS_CORRECT = 'is_correct'

    @classmethod
    def setUpClass(cls):
        super(BaseApiTestCase, cls).setUpClass()
        user = UserFactory(username='test_user', email='test@test.pl')
        user.set_password('test1234')
        for category_name in TEST_CATEGORIES:
            category = CategoryFactory(name=category_name)

    def setUp(self) -> None:
        super().setUp()
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user)


class AuthorizationApiTest(BaseAuthApiTestCase):
    def test_get_list_of_categories_when_user_is_not_authenticated(self) -> None:
        self._test_get('quiz:list-category', status.HTTP_401_UNAUTHORIZED)

    def test_list_quiz_when_user_is_not_authenticated(self) -> None:
        self._test_get('quiz:create-quiz', status.HTTP_401_UNAUTHORIZED)

    def test_create_quiz_when_user_is_not_authenticated(self) -> None:
        data = copy.deepcopy(DATA)
        self._test_post('quiz:create-quiz', status.HTTP_401_UNAUTHORIZED, data)

    def test_list_quizzes_on_homepage_when_user_is_not_authenticated(self) -> None:
        self._test_get('quiz:list-quiz', status.HTTP_200_OK)


class CategoryApiTest(BaseApiTestCase):
    def test_get_list_of_categories(self) -> None:
        response = self._test_get('quiz:list-category', status.HTTP_200_OK)
        self.assertCountEqual(response.data['categories'], TEST_CATEGORIES)
        self.assertListEqual(response.data['categories'], TEST_CATEGORIES)


class QuizApiTest(BaseApiTestCase):
    def _validation_quiz_handler(self, values, keys, expected_values, data, keys_of_data=None):
        if keys_of_data is None:
            keys_of_data = []

        tmp_data = data

        for k in keys_of_data:
            data = data[k]
        # print(data)
        for i, k in enumerate(keys):
            data[k] = values[i]

        response = self._test_post('quiz:create-quiz', status.HTTP_400_BAD_REQUEST, tmp_data)

        tmp_response = response.data
        # if len(keys_of_data) == 4:
        #     print(tmp_response)
        #     print(tmp_response['questions'][0]['answers'])
        for k in keys_of_data:
            if type(k) is int and len(tmp_response) == 1:
                break
            tmp_response = tmp_response[k]

        for i, key in enumerate(tmp_response):
            value = tmp_response[key]
            if type(value) is dict and 'error' in value:
                self.assertEqual(value['error'], expected_values[i])
            else:
                if type(value) is not ErrorDetail:
                    value = value[0]
                self.assertEqual(value, expected_values[i])

    def test_retrieve_quiz(self) -> None:
        create_test_data(2)

        response = self._test_get('quiz:retrieve-quiz', status.HTTP_200_OK, {'pk': 1})
        # quizzes = response.data['quizzes']
        data = response.data
        self.assertEqual(data['id'], 1)

    def test_retrieve_quiz_when_there_are_not_any_quizzes(self) -> None:
        self._test_get('quiz:retrieve-quiz', status.HTTP_404_NOT_FOUND, {'pk': 1})

    def test_create_quiz_with_valid_data(self) -> None:
        data = copy.deepcopy(DATA)

        response = self._test_post('quiz:create-quiz', status.HTTP_200_OK, data)
        self.assertEqual(response.data['message'], 'Quiz was created!')

    def test_validation_of_create_quiz_if_category_doesnt_exist(self) -> None:
        data = copy.deepcopy(DATA)
        keys = [self.CATEGORY]
        values = ['category']
        expected_values = ["Category doesn't exists!"]
        self._validation_quiz_handler(values, keys, expected_values, data)

    def test_validation_of_create_quiz_by_invalid_length_of_category(self) -> None:
        data = copy.deepcopy(DATA)
        keys = [self.CATEGORY]
        values = ['ca']
        expected_values = ['Ensure this field has at least 3 characters.']
        self._validation_quiz_handler(values, keys, expected_values, data)

    def test_validation_of_create_quiz_by_blanks_title_description_category_and_empty_list_of_the_questions(
            self) -> None:
        data = copy.deepcopy(DATA)
        keys = [self.TITLE, self.DESC, self.CATEGORY, self.QUESTIONS]
        values = ['', '', '', []]
        expected_values = ['This field may not be blank.' for _ in range(3)]
        expected_values.append('You need at least 3 questions to create quiz!!!')
        self._validation_quiz_handler(values, keys, expected_values, data)

    def test_validation_of_create_quiz_by_exceeded_numbers_of_questions_per_quiz(self) -> None:
        data = copy.deepcopy(DATA)
        questions = data['questions']
        question = copy.deepcopy(questions[0])
        [questions.append(copy.deepcopy(question)) for _ in range(30)]
        expected_values = [
            "You exceed the limit of questions per quiz, you can have maximum 20 questions per quiz. "]

        self._validation_quiz_handler([], [], expected_values, data)

    def test_validation_of_create_quiz_by_invalid_data_of_answer_and_is_correct_fields(self) -> None:
        data = copy.deepcopy(DATA)

        keys = [self.ANSWER, self.IS_CORRECT]
        values = ['', '']
        expected_values = ['Must be a valid boolean.', 'This field may not be blank.']

        self._validation_quiz_handler(values, keys, expected_values, data, keys_of_data=['questions', 0, 'answers', 2])

    def test_validation_of_create_quiz_by_lack_of_one_correct_answer_per_question(self) -> None:
        data = copy.deepcopy(DATA)
        keys = [self.ANSWER, self.IS_CORRECT]
        values = ['a', False]
        expected_values = ['You need at least one correct answer per question!!!']

        self._validation_quiz_handler(values, keys, expected_values, data, keys_of_data=['questions', 0, 'answers', 2])

    def test_validation_of_create_quiz_by_invalid_points_value_range(self) -> None:
        data = copy.deepcopy(DATA)
        keys = [self.POINTS]
        values = [1000]
        expected_values = ['The points must be between 1 to 5.']

        self._validation_quiz_handler(values, keys, expected_values, data, keys_of_data=['questions', 0])

    def test_validation_of_create_quiz_by_invalid_points_and_answers_and_question_value(self) -> None:
        data = copy.deepcopy(DATA)
        keys = [self.QUESTION, self.POINTS, self.ANSWERS]
        values = ['a', '', []]
        expected_values = ['Question must have at least 10 characters!!!', 'A valid integer is required.',
                           'You need at least 2 answers for each question to create quiz!!!']

        self._validation_quiz_handler(values, keys, expected_values, data, keys_of_data=['questions', 0])

    def test_validation_of_create_quiz_by_exceeded_numbers_of_answers(self) -> None:
        data = copy.deepcopy(DATA)

        answers = data['questions'][0]['answers']
        answer = {'answer': '1', 'is_correct': False}
        [answers.append(answer) for _ in range(6)]
        expected_values = [
            'You exceed the limit of answers for each question, you can have maximum 4 answers per question.']

        self._validation_quiz_handler([], [], expected_values, data, keys_of_data=['questions', 0])


class QuizListApiTest(BaseApiTestCase):
    def test_list_quiz(self) -> None:
        create_test_data(2)
        response = self._test_get('quiz:list-quiz', status.HTTP_200_OK)
        quizzes = response.data['quizzes']
        quizzes_data = response.data['quizzes'][0]

        self.assertEqual(len(quizzes), 2)
        self.assertEqual(quizzes_data['title'], 'It is an example')
        self.assertEqual(quizzes_data['num_of_questions'], 1)
        self.assertEqual(quizzes_data['owner'], 'test_user')

    def test_list_quiz_when_there_arent_any_quizzes(self) -> None:
        response = self._test_get('quiz:list-quiz', status.HTTP_200_OK)
        quizzes = response.data['quizzes']
        self.assertListEqual(quizzes, [])


class SolutionCreateApiTest(BaseApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        data = copy.deepcopy(DATA)
        self._test_post('quiz:create-quiz', status.HTTP_200_OK, data)

    def test_create_solution_of_quiz_with_valid(self) -> None:
        data = {
            "quiz_id": 1,
            "answers": [
                1, 5, 7
            ]
        }
        response = self._test_post('quiz:create-solution', status.HTTP_200_OK, data)
        self.assertEqual(response.data['message'], 'Solution was saved!')

    def test_validation_of_create_solution_of_quiz_by_invalid_answers_keys(self) -> None:
        data = {
            "quiz_id": 1,
            "answers": [
                1, 5, 79
            ]
        }
        response = self._test_post('quiz:create-solution', status.HTTP_400_BAD_REQUEST, data)
        self.assertEqual(response.data['answers'][0], 'Invalid pk "79" - object does not exist.')

    def test_validation_of_create_solution_of_quiz_by_invalid_quiz_id(self) -> None:
        data = {
            "quiz_id": 133,
            "answers": [
                1, 5, 7
            ]
        }
        response = self._test_post('quiz:create-solution', status.HTTP_400_BAD_REQUEST, data)
        self.assertEqual(response.data['quiz_id']['error'], 'Invalid quiz id passed! Quiz does not exist!!!')


class UsersSolutionsListApiTest(BaseApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        data = copy.deepcopy(DATA)
        self._test_post('quiz:create-quiz', status.HTTP_200_OK, data)

        quiz = Quiz.objects.get(pk=1)
        user = User.objects.get(username='test_user')
        answers = Answer.objects.filter(id__in=[1, 5, 7])
        SolutionFactory(quiz=quiz, solved_by=user, answers=answers)

    def test_list_users_solutions(self):
        response = self._test_get('quiz:list-users-solutions', status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        res = response.data[0]
        self.assertEqual(res['id'], 1)
        self.assertEqual(res['quiz']['title'], 'Basic knowledge')
        self.assertEqual(res['quiz']['category'], 'Mathematics')
