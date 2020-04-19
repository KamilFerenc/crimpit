from decimal import Decimal

from django.test import TestCase

from crimpit.results.factories import ResultFactory
from crimpit.results.models import ExerciseResult
from crimpit.tests.factories import TestSetFactory, ExerciseFactory
from crimpit.tests.models import HANGBOARD


class ExerciseResultTest(TestCase):
    def setUp(self) -> None:
        self.hangboard_exercise = ExerciseFactory(exercise_type=HANGBOARD)
        self.hangboard_test = TestSetFactory(test_type=HANGBOARD, exercises=[self.hangboard_exercise])
        self.result = ResultFactory(hangboard_test=self.hangboard_test)

    def test_save(self):
        result = ExerciseResult.objects.create(
            result=self.result,
            exercise=self.hangboard_exercise,
            left_hand=Decimal('3.67'),
            right_hand=Decimal('-2.63')
        )
        percent_left = ((self.result.athlete_weight - result.left_hand) / result.result.athlete_weight) * 100
        percent_right = ((self.result.athlete_weight - result.right_hand) / result.result.athlete_weight) * 100
        self.assertEqual(result.percent_left, percent_left)
        self.assertEqual(result.percent_right, percent_right)
