# Create your tests here.
import copy

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .factory import CategoryFactory, AnswerFactory, QuizFactory, QuestionFactory, TEST_CATEGORIES
from .test_data_dict import DATA


class BaseAuthApiTestCase(APITestCase):

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

    def setUp(self) -> None:
        super().setUp()
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user)



class AuthorizationApiTest(BaseAuthApiTestCase):
    def test_get_list_of_categories_when_user_is_not_authenticated(self) -> None:
        self._test_get('quiz:list-category', status.HTTP_401_UNAUTHORIZED)

    def test_list_quiz_when_user_is_not_authenticated(self) -> None:
        self._test_get('quiz:create-list-quiz', status.HTTP_401_UNAUTHORIZED)

    def test_create_quiz_when_user_is_not_authenticated(self) -> None:
        data = copy.deepcopy(DATA)
        self._test_post('quiz:create-list-quiz', status.HTTP_401_UNAUTHORIZED, data)


class CategoryApiTest(BaseApiTestCase):
    def test_get_list_of_categories(self) -> None:
        [CategoryFactory.create(category_name) for category_name in TEST_CATEGORIES]
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

        response = self._test_post('quiz:create-list-quiz', status.HTTP_400_BAD_REQUEST, tmp_data)

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

    def test_list_quiz_with_valid_data(self) -> None:
        [CategoryFactory.create(category_name) for category_name in TEST_CATEGORIES]
        user = User.objects.get(username='test_user')
        quiz = QuizFactory.create(user)
        question = QuestionFactory.create(quiz)
        AnswerFactory.create(question)
        AnswerFactory.create(question)

        response = self._test_get('quiz:create-list-quiz', status.HTTP_200_OK)
        quizzes = response.data['quizzes']
        self.assertEqual(len(quizzes), 1)

    def test_create_quiz_with_valid_data(self) -> None:
        CategoryFactory.create('Mathematics')
        data = copy.deepcopy(DATA)

        response = self._test_post('quiz:create-list-quiz', status.HTTP_200_OK, data)
        self.assertEqual(response.data['message'], 'Quiz was created!')

    def test_validation_of_create_quiz_if_category_doesnt_exist(self)->None:
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

    def test_validation_of_create_quiz_by_blanks_title_description_category_and_empty_list_of_the_questions(self) -> None:
        data = copy.deepcopy(DATA)
        keys = [self.TITLE, self.DESC, self.CATEGORY, self.QUESTIONS]
        values = ['', '', '', []]
        expected_values = ['This field may not be blank.' for _ in range(3)]
        expected_values.append('You need at least 3 questions to create quiz!!!')
        self._validation_quiz_handler(values, keys, expected_values, data)

    def test_validation_of_create_quiz_by_exceeded_numbers_of_questions_per_quiz(self) -> None:
        CategoryFactory.create('Mathematics')
        data = copy.deepcopy(DATA)
        questions = data['questions']
        question = copy.deepcopy(questions[0])
        [questions.append(copy.deepcopy(question)) for _ in range(30)]
        expected_values = [
            "You exceed the limit of questions per quiz, you can have maximum 20 questions per quiz. "]

        self._validation_quiz_handler([], [], expected_values, data)

    def test_validation_of_create_quiz_by_invalid_data_of_answer_and_is_correct_fields(self)->None:
        CategoryFactory.create('Mathematics')
        data = copy.deepcopy(DATA)

        keys = [self.ANSWER, self.IS_CORRECT]
        values = ['', '']
        expected_values = ['Must be a valid boolean.', 'This field may not be blank.']

        self._validation_quiz_handler(values, keys, expected_values, data, keys_of_data=['questions', 0, 'answers', 2])

    def test_validation_of_create_quiz_by_lack_of_one_correct_answer_per_question(self)->None:
        data = copy.deepcopy(DATA)
        keys = [self.ANSWER, self.IS_CORRECT]
        values = ['a', False]
        expected_values = ['You need at least one correct answer per question!!!']

        self._validation_quiz_handler(values, keys, expected_values, data, keys_of_data=['questions', 0, 'answers', 2])

    def test_validation_of_create_quiz_by_invalid_points_value_range(self) -> None:
        CategoryFactory.create('Mathematics')
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
