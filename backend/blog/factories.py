import factory
from django.utils import timezone
from users.factories import UserFactory

from .models import Post


class PostFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence')
    slug = factory.LazyAttribute(lambda obj: factory.Faker('slug', value=obj.title).generate())
    body = factory.Faker('paragraph', nb_sentences=50)
    author = factory.SubFactory(UserFactory)
    publish = factory.Faker('date_time_this_century', tzinfo=timezone.get_current_timezone())
    status = factory.Faker('random_element', elements=('draft', 'published'))

    class Meta:
        model = Post
