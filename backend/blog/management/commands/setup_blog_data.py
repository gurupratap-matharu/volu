"""A utility script to load dummy blog posts into the db"""

import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

import factory
from blog.factories import CommentFactory, PostFactory
from blog.models import Comment, Post

TAGS = ["hostel", "reception", "gardening", "organic farm", "vineyard", "ranch", "painting", "language",
        "hotel", "baby sitting", "construction", "bio farm", "fruit orchard", "ngo", "repair", "old age home", "cook", "cultural exchange"]

CustomUser = get_user_model()


class Command(BaseCommand):
    """
    Management command which cleans and populates database with mock data
    """

    help = "Loads fake blog posts data into the database"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "-l", "--locale", type=str, help="Define a locale for the data to be generated."
        )

    def handle(self, *args, **kwargs):
        locale = kwargs.get("locale")
        self.stdout.write(self.style.SUCCESS("Locale: %s" % locale))

        self.stdout.write(self.style.HTTP_BAD_REQUEST("Deleting old data..."))

        Post.objects.all().delete()
        Comment.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Creating new data..."))

        users = CustomUser.objects.all()

        with factory.Faker.override_default_locale(locale):

            posts = PostFactory.create_batch(size=100, author=random.choice(users))
            comments = CommentFactory.create_batch(size=500, post=random.choice(posts))

            for post in posts:
                tags = random.choices(TAGS, k=3)
                for tag in tags:
                    post.tags.add(tag)

        print(
            f"""
        Posts: {Post.objects.count()}
        Comments: {Comment.objects.count()}
        """
        )
        self.stdout.write(self.style.SUCCESS("All done! 💖💅🏻💫"))
