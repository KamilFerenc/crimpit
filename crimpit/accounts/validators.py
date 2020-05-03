from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_birth_date(value):
    if value >= timezone.datetime.today().date():
        raise ValidationError(_('Enter date from the past'))


def validate_start_climbing(value):
    if value > timezone.datetime.today().year:
        raise ValidationError(_('Enter current or earlier year'))
