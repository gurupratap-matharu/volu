import factory
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from faker import Faker

from .models import Profile

fake = Faker()


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
    country = factory.Faker('country_code')
    bio = factory.Faker('text')
    birth_date = factory.Faker('date_this_century')
    user = factory.SubFactory('users.factories.UserFactory', profile=None)


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(lambda obj: '%s-%s' % (obj.first_name, obj.last_name))
    email = factory.LazyAttribute(lambda obj: '%s-%s@email.com' % (obj.first_name.lower(), obj.last_name.lower()))
    profile = factory.RelatedFactory(ProfileFactory, factory_related_name='user')


def user_factory():
    user = UserFactory()

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
