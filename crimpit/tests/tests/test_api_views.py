import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from crimpit.accounts.factories import CustomUserFactory
from crimpit.helpers.tests.mixin import ViewTestMixin
from crimpit.tests.models import CampusTestSet


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
