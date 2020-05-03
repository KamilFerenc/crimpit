from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from crimpit.accounts.validators import validate_birth_date, validate_start_climbing


class ValidatorsTest(TestCase):
    def test_validate_birth_date(self):
        with self.assertRaises(ValidationError):
            validate_birth_date(timezone.datetime.today().date() + timezone.timedelta(days=2))

    def test_validate_start_climbing(self):
        with self.assertRaises(ValidationError):
            validate_start_climbing(timezone.datetime.today().year + 1)
