"""A utility script to load test data into the db for places app"""


import random

import factory
from places.factories import PlaceFactory, PlaceImageFactory
from places.models import Place, PlaceImage

from django.core.management.base import BaseCommand

TAGS = ["hostel", "reception", "gardening", "organic farm", "vineyard", "ranch", "painting", "language",
        "hotel", "baby sitting", "construction", "bio farm", "fruit orchard", "ngo", "repair", "old age home", "cook", "cultural exchange"]


class Command(BaseCommand):
    """
    Management command which cleans and populates database with mock data
    """

    help = "Loads fake places data into the database"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "-l", "--locale", type=str, help="Define a locale for the data to be generated."
        )

    def handle(self, *args, **kwargs):
        locale = kwargs.get("locale")
        self.stdout.write(self.style.SUCCESS("Locale: %s" % locale))

        self.stdout.write(self.style.HTTP_BAD_REQUEST("Deleting old data..."))
        Place.objects.all().delete()
        PlaceImage.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Creating new data..."))

        with factory.Faker.override_default_locale(locale):
            places = PlaceFactory.create_batch(size=50)

            for place in places:
                for _ in range(4):
                    PlaceImageFactory(place=place)

                tags = random.choices(TAGS, k=3)
                for tag in tags:
                    place.tags.add(tag)

        print(
            f"""
        Places: {Place.objects.count()}
        PlaceImages: {PlaceImage.objects.count()}
        """
        )
        self.stdout.write(self.style.SUCCESS("All done! 💖💅🏻💫"))
