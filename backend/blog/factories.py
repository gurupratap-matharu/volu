import factory
from users.factories import UserFactory, user_factory

from .models import Post


class PostFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence')
    slug = factory.Faker('slug', value=title)
    body = factory.Faker('paragraph', nb_sentences=50)
    author = factory.SubFactory(UserFactory)
    status = factory.Faker('random_element', elements=('draft', 'published'))

    class Meta:
        model = Post
