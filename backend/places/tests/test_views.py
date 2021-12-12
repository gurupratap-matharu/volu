from django.test import TestCase
from django.urls import resolve, reverse

from places.factories import PlaceFactory, PlaceImageFactory
from places.models import Place
from places.views import PlaceDetailView, SearchResultsView


class PlaceListTests(TestCase):
    pass


class PlaceDetailTests(TestCase):
    def setUp(self):
        self.place = PlaceFactory()
        self.images = PlaceImageFactory.create_batch(size=4, place=self.place)

    def test_place_detail_resolves_place_detail_view(self):
        view = resolve(self.place.get_absolute_url())
        self.assertEqual(PlaceDetailView.as_view().__name__, view.func.__name__)

    def test_place_detail_works(self):
        response = self.client.get(self.place.get_absolute_url())
        no_response = self.client.get('places/1234/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'places/place_detail.html')
        self.assertContains(response, self.place.name)
        self.assertContains(response, self.place.description)

        urls = [x.image.url for x in self.images]
        self.assertContains(response, urls)
        self.assertEqual(no_response.status_code, 404)
        self.assertNotContains(response, 'Hi I should not be on this page!')


class PlaceCreateTests(TestCase):
    pass


class PlaceUpdateTests(TestCase):
    pass


class PlaceDeleteTests(TestCase):
    pass


class PlaceSearchTests(TestCase):
    def test_place_search_works(self):
        response = self.client.get(reverse('places:search'))
        no_response = self.client.get('/place-search/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'places/search_results.html')
        self.assertContains(response, 'Search')
        self.assertNotContains(response, 'Hi I should not be on this page.')
        self.assertEqual(no_response.status_code, 404)

    def test_place_search_resolves_placesearchview(self):
        view = resolve(reverse('places:search'))
        self.assertEqual(view.func.__name__, SearchResultsView.as_view().__name__)
