from django.core.files.images import ImageFile
from django.test import TestCase
from places import models


class SignalTests(TestCase):
    """Test suite for all signals in places app."""

    def test_thumbnails_are_generated_on_save(self):
        pass