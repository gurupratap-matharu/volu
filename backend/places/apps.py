from django.apps import AppConfig


class PlacesConfig(AppConfig):
    name = 'places'

    def ready(self):
        from . import signals
