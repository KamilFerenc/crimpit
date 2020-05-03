from decimal import Decimal

from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from rest_auth.tests.mixins import APIClient

from crimpit.accounts.factories import CustomUserFactory
from crimpit.accounts.models import TRAINER
from crimpit.results.factories import HangboardResultFactory, ResultFactory, CampusResultFactory
from crimpit.results.serializers import ResultSerializer


class ResultSerializerTest(TestCase, APIClient):
    def setUp(self) -> None:
        self.serializer = ResultSerializer
        self.request = APIClient()
        self.user_1 = CustomUserFactory()
        self.user_2 = CustomUserFactory()
        self.user_2.athletes.add(self.user_1)
        self.request.user = self.user_2
        self.data = {
            'user': self.user_1.pk,
            'user_weight': Decimal('79.78')
        }

    def test_create_selected_user(self):
        serializer = self.serializer(data=self.data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        result = serializer.save()
        self.assertEqual(result.user, self.user_1)

    def test_create_user_from_request(self):
        del self.data['user']
        serializer = self.serializer(data=self.data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        result = serializer.save()
        self.assertEqual(result.user, self.user_2)

    def test_validate_user_valid(self):
        trainer = CustomUserFactory(type=TRAINER, athletes=[self.user_1])
        self.request.user = trainer
        serializer = self.serializer(data=self.data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())

    def test_validate_user_invalid(self):
        self.data['user'] = self.user_2.pk
        trainer = CustomUserFactory(type=TRAINER, athletes=[self.user_1])
        self.request.user = trainer
        serializer = self.serializer(data=self.data, context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn(*serializer.errors['user'], _('You can\'t create result for user who is not your athlete.'))

    def test_update_hangboard_results(self):
        result = ResultFactory()
        hangboard_result = HangboardResultFactory(result=result, left_hand=None, right_hand=None)
        data = {
            'hangboard_results': [
                {'pk': hangboard_result.pk, 'left_hand': Decimal('23.12'), 'right_hand': Decimal('13.33')},
            ]
        }
        serializer = self.serializer(instance=result, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        hangboard_result.refresh_from_db()
        self.assertEqual(hangboard_result.left_hand, data['hangboard_results'][0]['left_hand'])
        self.assertEqual(hangboard_result.right_hand, data['hangboard_results'][0]['right_hand'])

    def test_update_hangboard_results_invalid_pk(self):
        result = ResultFactory()
        hangboard_result = HangboardResultFactory(result=result, left_hand=Decimal('12.69'), right_hand=None)
        result_left = hangboard_result.left_hand
        result_right = hangboard_result.right_hand
        data = {
            'hangboard_results': [
                {'pk': 0, 'left_hand': Decimal('23.12'), 'right_hand': Decimal('13.33')},
            ]
        }
        serializer = self.serializer(instance=result, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(hangboard_result.left_hand, result_left)
        self.assertEqual(hangboard_result.right_hand, result_right)

    def test_update_campus_results(self):
        result = ResultFactory()
        campus_results = CampusResultFactory(result=result, moves=12)
        data = {
            'campus_results': [
                {'pk': campus_results.pk, 'moves': 15},
            ]
        }
        serializer = self.serializer(instance=result, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        campus_results.refresh_from_db()
        self.assertEqual(campus_results.moves, data['campus_results'][0]['moves'])

    def test_update_campus_results_invalid_pk(self):
        result = ResultFactory()
        campus_results = CampusResultFactory(result=result, moves=12)
        result_moves = campus_results.moves
        data = {
            'campus_results': [
                {'pk': 0, 'moves': 15},
            ]
        }
        serializer = self.serializer(instance=result, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        campus_results.refresh_from_db()
        self.assertEqual(campus_results.moves, result_moves)
