import factory

from crimpit.accounts.models import Athlete


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Athlete

    username = factory.Sequence(lambda n: f'User_{n}')
    club = factory.Sequence(lambda n: f'Club_{n}')
