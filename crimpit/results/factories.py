from decimal import Decimal

import factory

from crimpit.accounts.factories import CustomUserFactory
from crimpit.results.models import Result


class ResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Result

    athlete = factory.SubFactory(CustomUserFactory)
    athlete_weight = Decimal('100.00')
