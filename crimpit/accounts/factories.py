import factory
from django.contrib.auth.models import User

from crimpit.accounts.models import CustomUser


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'User_{n}')
    email = factory.Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'pass')


class CustomUserFactory(UserFactory):
    class Meta:
        model = CustomUser

    club = factory.Sequence(lambda n: f'Club_{n}')

    @factory.post_generation
    def tests(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for test in extracted:
                self.tests.add(test)

    @factory.post_generation
    def athletes(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for athlete in extracted:
                self.athletes.add(athlete)
