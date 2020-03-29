from django.test import TestCase

from crimpit.accounts.factories import CustomUserFactory
from crimpit.tests.models import TestSet, Exercise
from crimpit.tests.serializers import TestSetSerializer, ExerciseSerializer


class TestSetSerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer = TestSetSerializer
        self.user = CustomUserFactory()
        self.data = {
            'title': 'Test title',
            'creator': self.user.pk,
        }

    def test_valid_data(self):
        serializer = self.serializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(TestSet.objects.first().title, self.data['title'])
        self.assertEqual(TestSet.objects.first().creator, self.user)

    def test_invalid_data(self):
        del self.data['title']
        serializer = self.serializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)


class ExerciseSerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer = ExerciseSerializer
        self.user = CustomUserFactory()
        self.data = {
            'title': 'Test title exercise',
            'creator': self.user.pk,
        }

    def test_valid_data(self):
        serializer = self.serializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Exercise.objects.first().title, self.data['title'])
        self.assertEqual(Exercise.objects.first().creator, self.user)

    def test_invalid_data(self):
        del self.data['title']
        serializer = self.serializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
