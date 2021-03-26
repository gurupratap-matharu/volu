from os import name

import factory
from django.utils import timezone
from users.factories import UserFactory

from .models import Comment, Post


class PostFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('sentence')
    slug = factory.LazyAttribute(lambda obj: factory.Faker('slug', value=obj.title).generate())
    body = factory.Faker('paragraph', nb_sentences=50)
    author = factory.SubFactory(UserFactory)
    publish = factory.Faker('date_time_this_century', tzinfo=timezone.get_current_timezone())
    status = factory.Faker('random_element', elements=('draft', 'published'))

    class Meta:
        model = Post


class CommentFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    email = factory.Faker('email')
    body = factory.Faker('paragraph', nb_sentences=5)
    post = factory.SubFactory(PostFactory)

    class Meta:
        model = Comment
