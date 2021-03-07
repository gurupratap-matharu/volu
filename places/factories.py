import factory
from users.factories import AbstractUserFactory

from places.models import Place

NAMES = ['Hostel', 'Beautiful House', 'Wineyard', 'Organic Farm', 'Country Cabin']


class PlaceFactory(factory.django.DjangoModelFactory):

    name = factory.Faker('random_element', elements=NAMES)
    description = factory.Faker('text')
    email = factory.Faker('email')
    address1 = factory.Faker('address')
    address2 = factory.Faker('address')
    city = factory.Faker('city')
    zip_code = factory.Faker('zipcode')
    country = factory.Faker('country_code')
    host = factory.SubFactory(AbstractUserFactory)

    class Meta:
        model = Place
