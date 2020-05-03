import json
from decimal import Decimal

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework.test import APIClient

from crimpit.accounts.factories import CustomUserFactory
from crimpit.accounts.models import TRAINER
from crimpit.helpers.tests.mixin import ViewTestMixin
from crimpit.results.api_view import BaseResultView
from crimpit.results.factories import ResultFactory
from crimpit.tests.factories import TestSetFactory, ExerciseFactory
from crimpit.tests.models import CAMPUS_BOARD, HANGBOARD


class BaseResultViewTest(ViewTestMixin, TestCase, APIClient):
    def setUp(self) -> None:
        self.athletes_1 = CustomUserFactory()
        self.athletes_2 = CustomUserFactory()
        self.trainer = CustomUserFactory(type=TRAINER, athletes=[self.athletes_1, self.athletes_2])
        self.result_1 = ResultFactory(user=self.athletes_1)
        self.result_2 = ResultFactory(user=self.athletes_2)
        self.result_3 = ResultFactory()
        self.request = RequestFactory()

    def test_get_queryset_athlete_1(self):
        self.request.user = self.athletes_1
        view = BaseResultView()
        view.setup(self.request)
        self.assertEqual(view.get_queryset().count(), 1)
        self.assertEqual(view.get_queryset().first(), self.result_1)

    def test_get_queryset_athlete_2(self):
        self.request.user = self.athletes_2
        view = BaseResultView()
        view.setup(self.request)
        self.assertEqual(view.get_queryset().count(), 1)
        self.assertEqual(view.get_queryset().first(), self.result_2)

    def test_get_queryset_trainer(self):
        self.request.user = self.trainer
        view = BaseResultView()
        view.setup(self.request)
        results = view.get_queryset()
        self.assertEqual(results.count(), 2)
        self.assertIn(self.result_1, results)
        self.assertIn(self.result_2, results)


class StartTestViewTest(ViewTestMixin, TestCase, APIClient):
    def setUp(self) -> None:
        self.user = CustomUserFactory()
        self.url = reverse('start_test')
        self.client = APIClient()
        self.login(self.user)
        self.campus_exercise = ExerciseFactory(creator=self.user, exercise_type=CAMPUS_BOARD)
        self.hangboard_exercise = ExerciseFactory(creator=self.user, exercise_type=HANGBOARD)
        self.campus_test = TestSetFactory(creator=self.user, test_type=CAMPUS_BOARD, exercises=[self.campus_exercise])
        self.hangboard_test = TestSetFactory(creator=self.user,
                                             test_type=HANGBOARD,
                                             exercises=[self.hangboard_exercise])
        self.data = {
            'campus_test': self.campus_test.pk,
            'hangboard_test': self.hangboard_test.pk,
            'user_weight': Decimal('65.43')
        }

    def test_valid_data(self):
        resp = self.client.post(self.url, data=self.data)
        self.assertEqual(resp.status_code, 201)
        result = json.loads(resp.content)
        self.assertEqual(result['user'], self.user.pk)
        self.assertEqual(result['campus_test'], self.campus_test.pk)
        self.assertEqual(result['hangboard_test'], self.hangboard_test.pk)
        self.assertEqual(result['hangboard_results'][0]['exercise']['title'], self.hangboard_exercise.title)
        self.assertEqual(result['campus_results'][0]['exercise']['title'], self.campus_exercise.title)

    def test_invalid_data_empty_user_weight(self):
        del self.data['user_weight']
        resp = self.client.post(self.url, data=self.data)
        result = json.loads(resp.content)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(result['user_weight'][0], _('This field is required.'))
