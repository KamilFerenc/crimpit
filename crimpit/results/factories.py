import factory.fuzzy

from crimpit.accounts.factories import CustomUserFactory
from crimpit.results.models import Result, CampusResult, HangboardResult
from crimpit.tests.factories import ExerciseFactory


class ResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Result

    user = factory.SubFactory(CustomUserFactory)
    user_weight = factory.fuzzy.FuzzyDecimal(60, 100)


class CampusResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CampusResult

    exercise = factory.SubFactory(ExerciseFactory)
    moves = factory.fuzzy.FuzzyInteger(1, 100)


class HangboardResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HangboardResult

    exercise = factory.SubFactory(ExerciseFactory)
    right_hand = factory.fuzzy.FuzzyDecimal(0, 30)
    left_hand = factory.fuzzy.FuzzyDecimal(0, 30)
