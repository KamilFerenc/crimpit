import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from crimpit.accounts.factories import CustomUserFactory
from crimpit.helpers.tests.mixin import ViewTestMixin
from crimpit.tests.factories import TestSetFactory, ExerciseFactory


class IsCreatorOrReadOnlyTest(ViewTestMixin, TestCase, APIClient):
    def setUp(self) -> None:
        self.owner = CustomUserFactory()
        self.user = CustomUserFactory()
        self.client = APIClient()
        self.test = TestSetFactory(creator=self.owner)
        self.exercise = ExerciseFactory()
        self.data = {
            'title': 'New title'
        }

    def test_patch_creator(self):
        self.login(self.owner)
        resp = self.client.patch(reverse('hangboard_test_detail', kwargs={'pk': self.test.pk}), data=self.data)
        self.assert_resp_ok(resp)
        self.test.refresh_from_db()
        self.assertEqual(self.test.title, self.data['title'])

    def test_patch_creator_add_exercise(self):
        data = {'exercises': [self.exercise.pk]}
        self.login(self.owner)
        resp = self.client.patch(reverse('add_exercise', kwargs={'pk': self.test.pk}), data=data)
        self.assert_resp_ok(resp)
        self.test.refresh_from_db()
        self.assertEqual(self.test.exercises.all().count(), 1)
        self.assertEqual(self.test.exercises.first(), self.exercise)

    def test_patch_user(self):
        self.login(self.user)
        resp = self.client.patch(reverse('hangboard_test_detail', kwargs={'pk': self.test.pk}), data=self.data)
        self.assertEqual(resp.status_code, 403)

    def test_patch_user_add_exercise(self):
        data = {'exercises': [self.exercise.pk]}
        self.login(self.owner)
        resp = self.client.patch(reverse('add_exercise', kwargs={'pk': self.test.pk}), data=data)
        self.assert_resp_ok(resp)
        self.test.refresh_from_db()
        self.assertEqual(self.test.exercises.all().count(), 1)
        self.assertEqual(self.test.exercises.first(), self.exercise)

    def test_get_user(self):
        self.login(self.user)
        resp = self.client.get(reverse('hangboard_test_detail', kwargs={'pk': self.test.pk}))
        result = json.loads(resp.content)
        self.assert_resp_ok(resp)
        self.assertEqual(result['title'], self.test.title)
