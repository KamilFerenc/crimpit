from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from crimpit.results.validators import check_if_positive


class CheckIfPositiveTest(TestCase):
    def test_check_if_positive(self):
        self.assertIsNone(check_if_positive(Decimal('1.32')))

    def test_check_if_positive_invalid_value(self):
        with self.assertRaises(ValidationError):
            check_if_positive(Decimal('-123.32'))
