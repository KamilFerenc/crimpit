from django.test import TestCase, RequestFactory

from django.utils import timezone

from crimpit.accounts.factories import CustomUserFactory
from crimpit.accounts.models import TRAINER
from crimpit.accounts.serializers import CustomUserSerializer, AddTestSerializer, DeleteTestSerializer
from crimpit.tests.factories import TestSetFactory
from crimpit.tests.models import TestSet


class CustomUserSerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer = CustomUserSerializer
        self.data = {
            'username': 'test_username',
            'email': 'test@test.com',
            'password': 'password',
            'password_2': 'password',
            'type': TRAINER,
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


class AddTestSerializerTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory()
        self.test = TestSetFactory()
        self.data = {
            'tests': [self.test.pk]
        }
        self.serializer = AddTestSerializer
        self.request = RequestFactory()
        self.request.user = self.user
        self.context = {
            "request": self.request,
        }

    def test_valid_data(self):
        self.assertEqual(self.user.tests.count(), 0)
        serializer = self.serializer(instance=self.user, data=self.data, context=self.context)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.tests.count(), 1)
        self.assertEqual(self.user.tests.first(), self.test)

    def test_invalid_data_test_not_exists(self):
        self.data['tests'] = [TestSet.objects.count() + 1]
        self.assertEqual(self.user.tests.count(), 0)
        serializer = self.serializer(instance=self.user, data=self.data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tests', serializer.errors)
        self.assertEqual(serializer.errors['tests'][0].code, 'does_not_exist')


class DeleteTestSerializerTest(TestCase):
    def setUp(self) -> None:
        self.test = TestSetFactory()
        self.user = CustomUserFactory(tests=[self.test])
        self.data = {
            'tests': [self.test.pk]
        }
        self.serializer = DeleteTestSerializer
        self.request = RequestFactory()
        self.request.user = self.user
        self.context = {
            "request": self.request,
        }

    def test_valid_data(self):
        self.assertEqual(self.user.tests.count(), 1)
        self.assertEqual(self.user.tests.first(), self.test)
        serializer = self.serializer(instance=self.user, data=self.data, context=self.context)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.tests.count(), 0)

    def test_invalid_data_test_not_exists(self):
        self.data['tests'] = [TestSet.objects.count() + 1]
        self.assertEqual(self.user.tests.count(), 1)
        serializer = self.serializer(instance=self.user, data=self.data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tests', serializer.errors)
        self.assertEqual(serializer.errors['tests'][0].code, 'does_not_exist')
        self.assertEqual(self.user.tests.count(), 1)
