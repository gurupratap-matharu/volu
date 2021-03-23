import factory
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()


class AbstractUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    username = factory.Faker('user_name')


def user_factory():
    user = AbstractUserFactory()

    user.profile.country = fake.country_code()
    user.profile.bio = fake.text()
    user.profile.birth_date = fake.date()

    user.save()
    return user


def superuser_factory():
    superuser = get_user_model().objects.create_superuser(
        username='superuser',
        email='superuser@email.com',
        password='superpass123'
    )
    return superuser
