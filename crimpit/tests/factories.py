import factory

from crimpit.accounts.factories import CustomUserFactory
from crimpit.tests.models import TestSet, Exercise


class TestSetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TestSet

    title = factory.Sequence(lambda n: f'Title_{n}')
    creator = factory.SubFactory(CustomUserFactory)

    @factory.post_generation
    def exercises(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for exercise in extracted:
                self.exercises.add(exercise)


class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exercise

    title = factory.Sequence(lambda n: f'Exercise_{n}')
    creator = factory.SubFactory(CustomUserFactory)
