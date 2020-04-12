import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from crimpit.accounts.factories import CustomUserFactory
from crimpit.helpers.tests.mixin import ViewTestMixin


class IsOwnerOrReadOnlyTest(ViewTestMixin, TestCase, APIClient):
    def setUp(self) -> None:
        self.owner = CustomUserFactory()
        self.user = CustomUserFactory()
        self.client = APIClient()
        self.data = {
            'club': 'test_club'
        }

    def test_patch_owner(self):
        self.login(self.owner)
        resp = self.client.patch(reverse('user_detail', kwargs={'pk': self.owner.pk}), data=self.data)
        self.assert_resp_ok(resp)
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.club, self.data['club'])

    def test_patch_user(self):
        self.login(self.user)
        resp = self.client.patch(reverse('user_detail', kwargs={'pk': self.owner.pk}), data=self.data)
        self.assertEqual(resp.status_code, 403)

    def test_get_user(self):
        self.login(self.user)
        resp = self.client.get(reverse('user_detail', kwargs={'pk': self.owner.pk}))
        result = json.loads(resp.content)
        self.assert_resp_ok(resp)
        self.assertEqual(result['username'], self.owner.username)
