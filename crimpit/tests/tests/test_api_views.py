import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from crimpit.accounts.factories import CustomUserFactory
from crimpit.helpers.tests.mixin import ViewTestMixin
from crimpit.tests.factories import TestSetFactory, ExerciseFactory
from crimpit.tests.models import CampusTestSet, CAMPUS_BOARD, HANGBOARD


class CampusTestSetApiViewTest(ViewTestMixin, TestCase, APIClient):
    def setUp(self) -> None:
        self.user = CustomUserFactory()
        self.data = {
            'title': 'Test title',
            'test_type': 'campus_board'
        }
        self.login(self.user)
        self.url = reverse('campus_tests_list')

    def test_post_valid_data(self):
        resp = self.client.post(self.url, data=self.data)
        result = json.loads(resp.content)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(result['title'], self.data['title'])
        self.assertEqual(CampusTestSet.objects.first().title, self.data['title'])
        self.assertEqual(CampusTestSet.objects.first().creator, self.user)


class AddExerciseApiViewTest(ViewTestMixin, TestCase, APIClient):
    def setUp(self) -> None:
        self.user = CustomUserFactory()
        self.test_campus = TestSetFactory(test_type=CAMPUS_BOARD, creator=self.user)
        self.campus_exercise = ExerciseFactory(exercise_type=CAMPUS_BOARD, creator=self.user)
        self.hangboard_exercise = ExerciseFactory(exercise_type=HANGBOARD, creator=self.user)
        self.data = {'exercises': [self.campus_exercise.pk]}
        self.login(self.user)
        self.url = reverse('add_exercise', kwargs={'pk': self.test_campus.pk})

    def test_valid_data(self):
        self.assertEqual(self.test_campus.exercises.all().count(), 0)
        resp = self.client.patch(self.url, data=self.data, content_type="application/json")
        self.assert_resp_ok(resp)
        self.test_campus.refresh_from_db()
        self.assertEqual(self.test_campus.exercises.all().count(), 1)
        self.assertEqual(self.test_campus.exercises.first(), self.campus_exercise)

    def test_exercise_different_type(self):
        self.assertEqual(self.test_campus.exercises.all().count(), 0)
        self.data['exercises'] = [self.hangboard_exercise.pk, ]
        resp = self.client.patch(self.url, data=self.data, content_type="application/json")
        self.assertEqual(resp.status_code, 400)
        self.test_campus.refresh_from_db()
        self.assertEqual(self.test_campus.exercises.all().count(), 0)


class DeleteExerciseApiViewTest(ViewTestMixin, TestCase, APIClient):
    def setUp(self) -> None:
        self.user = CustomUserFactory()
        self.campus_exercise_1 = ExerciseFactory(exercise_type=CAMPUS_BOARD, creator=self.user)
        self.campus_exercise_2 = ExerciseFactory(exercise_type=CAMPUS_BOARD, creator=self.user)
        self.test_campus = TestSetFactory(
            test_type=CAMPUS_BOARD,
            creator=self.user,
            exercises=[self.campus_exercise_1, self.campus_exercise_2]
        )
        self.hangboard_exercise = ExerciseFactory(exercise_type=HANGBOARD, creator=self.user)
        self.data = {'exercises': [self.campus_exercise_1.pk]}
        self.login(self.user)
        self.url = reverse('delete_exercise', kwargs={'pk': self.test_campus.pk})

    def test_valid_data(self):
        self.assertEqual(self.test_campus.exercises.all().count(), 2)
        resp = self.client.patch(self.url, data=self.data, content_type="application/json")
        self.assert_resp_ok(resp)
        self.test_campus.refresh_from_db()
        self.assertEqual(self.test_campus.exercises.all().count(), 1)
        self.assertEqual(self.test_campus.exercises.first(), self.campus_exercise_2)

    def test_exercise_different_type(self):
        self.assertEqual(self.test_campus.exercises.all().count(), 2)
        self.data['exercises'] = [self.hangboard_exercise.pk]  # exercise does't belong to the test
        resp = self.client.patch(self.url, data=self.data, content_type="application/json")
        self.assert_resp_ok(resp)
        self.test_campus.refresh_from_db()
        self.assertEqual(self.test_campus.exercises.all().count(), 2)
        self.assertIn(self.campus_exercise_1, self.test_campus.exercises.all())
        self.assertIn(self.campus_exercise_2, self.test_campus.exercises.all())
