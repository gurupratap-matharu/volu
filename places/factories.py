import factory
from users.factories import AbstractUserFactory

from places.models import Place


class PlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Place

    name = factory.Faker('catch_phrase')
    description = factory.Faker('text')
    email = factory.Faker('company_email')
    address1 = factory.Faker('address')
    address2 = factory.Faker('address')
    city = factory.Faker('city')
    zip_code = factory.Faker('zipcode')
    country = factory.Faker('country_code')
    host = factory.SubFactory(AbstractUserFactory)
