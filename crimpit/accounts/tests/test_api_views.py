from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from crimpit.accounts.factories import UserFactory
from crimpit.accounts.models import TRAINER, CustomUser


class CreateUserApiTest(TestCase, APIClient):
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
        self.athlete_1 = UserFactory()
        self.athlete_2 = UserFactory()
        self.client = APIClient()

    def test_get_request(self):
        resp = self.client.get(reverse('athletes-list'))
        self.assertEqual(resp.status_code, 403)
