from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def check_if_positive(value):
    if value <= 0:
        raise ValidationError(_('Weight has to be greater than 0.'))
