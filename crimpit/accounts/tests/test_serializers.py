from django.test import TestCase

from django.utils import timezone

from crimpit.accounts.models import COACH, CustomUser
from crimpit.accounts.serializers import CustomUserSerializer


class CustomUserSerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer = CustomUserSerializer
        self.data = {
            'username': 'test_username',
            'email': 'test@test.com',
            'password': 'password',
            'password_2': 'password',
            'type': COACH,
            'club': 'KS KORONA'
        }

    def test_valid_data(self):
        serializer = self.serializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, self.data['username'])
        self.assertEqual(user.email, self.data['email'])
        self.assertEqual(user.type, self.data['type'])
        self.assertEqual(user.club, self.data['club'])

    def test_invalid_password_2(self):
        self.data['password_2'] = 'password_2'
        serializer = self.serializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['password'][0].code, 'invalid')
        self.assertEqual(serializer.errors['password_2'][0].code, 'invalid')

    def test_invalid_type(self):
        self.data['type'] = 'invalid'
        serializer = self.serializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['type'][0].code, 'invalid_choice')

    def test_empty_club(self):
        del self.data['club']
        serializer = self.serializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['club'][0].code, 'required')

    def test_invalid_start_climbing(self):
        self.data['start_climbing'] = timezone.datetime.today().year + 1
        serializer = self.serializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['start_climbing'][0].code, 'invalid')

    def test_invalid_birth_date(self):
        self.data['birth_date'] = timezone.datetime.today() + timezone.timedelta(days=1)
        serializer = self.serializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['birth_date'][0].code, 'datetime')
