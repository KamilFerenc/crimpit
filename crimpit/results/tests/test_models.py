from decimal import Decimal, ROUND_HALF_UP

from django.test import TestCase
from django.utils import timezone

from crimpit.accounts.factories import CustomUserFactory
from crimpit.results.factories import ResultFactory
from crimpit.results.models import HangboardResult
from crimpit.tests.factories import TestSetFactory, ExerciseFactory
from crimpit.tests.models import HANGBOARD


class ExerciseResultTest(TestCase):
    def setUp(self) -> None:
        self.hangboard_exercise = ExerciseFactory(exercise_type=HANGBOARD)
        self.hangboard_test = TestSetFactory(test_type=HANGBOARD, exercises=[self.hangboard_exercise])
        self.result = ResultFactory(hangboard_test=self.hangboard_test)

    def test_save(self):
        result = HangboardResult.objects.create(
            result=self.result,
            exercise=self.hangboard_exercise,
            left_hand=Decimal('3.67'),
            right_hand=Decimal('-2.63')
        )
        percent_left = (((self.result.user_weight - result.left_hand) / result.result.user_weight) * 100).quantize(
            Decimal('.01'), rounding=ROUND_HALF_UP)
        percent_right = (((self.result.user_weight - result.right_hand) / result.result.user_weight) * 100).quantize(
            Decimal('.01'), rounding=ROUND_HALF_UP)
        self.assertEqual(result.percent_left, percent_left)
        self.assertEqual(result.percent_right, percent_right)


class ResultTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory()
        self.created = timezone.now()
        self.result = ResultFactory(user=self.user, created=self.created)

    def test__str__(self):
        self.assertEqual(str(self.result),
                         f'Result {self.result.pk}: {self.user.username} ({self.created.strftime("%Y-%m-%d")})')
