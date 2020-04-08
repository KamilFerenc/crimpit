import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from crimpit.accounts.factories import CustomUserFactory
from crimpit.accounts.models import TRAINER, CustomUser, ATHLETE
from crimpit.helpers.tests.mixin import ViewTestMixin


class CreateUserApiTest(ViewTestMixin, TestCase, APIClient):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            'username': 'test_username',
            'email': 'test@test.com',
            'password': 'password',
            'password_2': 'password',
            'type': TRAINER,
            'club': 'KS KORONA'
        }

    def test_login(self):
        user = CustomUserFactory(username='test', password='test')
        resp = self.client.post(reverse('rest_login'), data={'username': 'test', 'password': 'test'})
        self.assert_resp_ok(resp)
        result = json.loads(resp.content)
        self.assertEqual(result['key'], user.auth_token.key)

    def test_get_request(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 405)

    def test_valid_data(self):
        resp = self.client.post(reverse('register'), data=self.data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(CustomUser.objects.count(), 1)
        user = CustomUser.objects.first()
        self.assertEqual(user.username, self.data['username'])
        self.assertEqual(user.email, self.data['email'])
        self.assertEqual(user.club, self.data['club'])
        self.assertEqual(user.type, self.data['type'])

    def test_invalid_type(self):
        self.data['type'] = 'test'
        resp = self.client.post(reverse('register'), data=self.data)
        self.assertEqual(resp.status_code, 400)
        self.assertIn('type', str(resp.content))

    def test_password_not_match(self):
        self.data['password_2'] = 'password_2'
        resp = self.client.post(reverse('register'), data=self.data)
        self.assertEqual(resp.status_code, 400)
        self.assertIn('password', str(resp.content))
        self.assertIn('password_2', str(resp.content))


class AthletesListTest(TestCase, APIClient):
    def setUp(self):
        self.athlete_1 = CustomUserFactory()
        self.athlete_2 = CustomUserFactory()
        self.client = APIClient()

    def test_get_request(self):
        resp = self.client.get(reverse('athletes_list'))
        self.assertEqual(resp.status_code, 403)


class DetailUpdateUserApiViewTest(ViewTestMixin, TestCase, APIClient):
    def setUp(self) -> None:
        self.tmp_file = self.crete_image()
        self.data = {
            'club': 'new_club',
            'type': ATHLETE,
        }
        self.user = CustomUserFactory(profile_photo=self.tmp_file.name)
        self.client = APIClient()
        self.login(self.user)
        self.url = reverse('user_detail', kwargs={'pk': self.user.pk})

    def test_valid_data(self):
        resp = self.client.patch(self.url, data=self.data, format='multipart')
        self.assert_resp_ok(resp)
        self.user.refresh_from_db()
        self.assertEqual(self.user.club, self.data['club'])
        self.assertEqual(self.user.type, self.data['type'])

    def test_invalid_type(self):
        self.data['type'] = 'test'
        resp = self.client.patch(self.url, data=self.data, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('type', str(resp.content))

    def test_empty_club(self):
        self.data['club'] = ''
        resp = self.client.patch(self.url, data=self.data, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('club', str(resp.content))
