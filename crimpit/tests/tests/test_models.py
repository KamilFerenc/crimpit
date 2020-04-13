from django.test import TestCase

from crimpit.tests.factories import TestSetFactory, ExerciseFactory


class TestSetTest(TestCase):
    def setUp(self) -> None:
        self.test = TestSetFactory()

    def test__str__(self):
        self.assertEqual(str(self.test), f'{self.test.pk} - {self.test.title}')


class ExerciseTest(TestCase):
    def setUp(self) -> None:
        self.test = ExerciseFactory()

    def test__str__(self):
        self.assertEqual(str(self.test), f'{self.test.pk} - {self.test.title}')
