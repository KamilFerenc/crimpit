from crimpit.tests.factories import TestSetFactory, ExerciseFactory
from crimpit.tests.models import CAMPUS_BOARD, HANGBOARD
from crimpit.tests.serializers import AddExerciseSerializer

from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient

from crimpit.accounts.factories import CustomUserFactory
from crimpit.helpers.tests.mixin import ViewTestMixin
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
        self.request = RequestFactory()
        self.request.user = self.user
        self.context = {
            "request": self.request,
        }

    def test_valid_data(self):
        serializer = self.serializer(data=self.data, context=self.context)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(TestSet.objects.first().title, self.data['title'])
        self.assertEqual(TestSet.objects.first().creator, self.user)

    def test_invalid_data(self):
        del self.data['title']
        serializer = self.serializer(data=self.data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)


class ExerciseSerializerTest(ViewTestMixin, TestCase, APIClient):
    def setUp(self) -> None:
        self.serializer = ExerciseSerializer
        self.user = CustomUserFactory()
        self.client = APIClient
        self.data = {
            'title': 'Test title exercise',
            'creator': self.user.pk,
        }
        self.request = RequestFactory()
        self.request.user = self.user
        self.context = {
            "request": self.request,
        }

    def test_valid_data(self):
        serializer = self.serializer(data=self.data, context=self.context)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Exercise.objects.first().title, self.data['title'])
        self.assertEqual(Exercise.objects.first().creator, self.user)

    def test_invalid_data(self):
        del self.data['title']
        serializer = self.serializer(data=self.data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)


class AddExerciseSerializerTest(TestCase):
    def setUp(self) -> None:
        self.campus_test = TestSetFactory(test_type=CAMPUS_BOARD)
        self.hangboard_test = TestSetFactory(test_type=HANGBOARD)
        self.campus_exercise = ExerciseFactory(exercise_type=CAMPUS_BOARD)
        self.hangboard_exercise = ExerciseFactory(exercise_type=HANGBOARD)
        self.serializer = AddExerciseSerializer

    def test_valid_data(self):
        self.assertEqual(self.campus_test.exercises.count(), 0)
        data = {'exercises': [self.campus_exercise.pk]}
        context = {'test_type': self.campus_test.test_type}
        serializer = self.serializer(instance=self.campus_test, data=data, context=context)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.campus_test.refresh_from_db()
        self.assertEqual(self.campus_test.exercises.count(), 1)
        self.assertEqual(self.campus_test.exercises.first(), self.campus_exercise)

    def test_invalid_data_different_type(self):
        self.assertEqual(self.hangboard_test.exercises.count(), 0)
        data = {'exercises': [self.campus_exercise.pk]}
        context = {'test_type': self.hangboard_test.test_type}
        serializer = self.serializer(instance=self.hangboard_test, data=data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('exercises', serializer.errors)
