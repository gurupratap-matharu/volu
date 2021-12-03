import factory
from places.models import Place, PlaceImage
from users.factories import UserFactory

from django.core.files.base import ContentFile

NAMES = ['Hostel', 'Beautiful House', 'Wineyard', 'Organic Farm', 'Country Cabin']


class PlaceFactory(factory.django.DjangoModelFactory):

    name = factory.Faker('city')
    slug = factory.LazyAttribute(lambda obj: factory.Faker('slug', value=obj.name).generate())
    description = factory.Faker('text')
    email = factory.Faker('email')
    address1 = factory.Faker('address')
    address2 = factory.Faker('address')
    city = factory.Faker('city')
    zip_code = factory.Faker('zipcode')
    country = factory.Faker('country_code')
    ratings = factory.Faker('random_int', min=0, max=1000)
    host = factory.SubFactory(UserFactory)

    class Meta:
        model = Place


class PlaceImageFactory(factory.django.DjangoModelFactory):
    place = factory.SubFactory(PlaceFactory)
    # image = factory.django.ImageField(color='blue')
    image = ContentFile(factory.django.ImageField()._make_data(
        {'width': 1024, 'height': 768}), 'example.jpg')

    class Meta:
        model = PlaceImage
