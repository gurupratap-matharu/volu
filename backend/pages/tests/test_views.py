from django.test import TestCase
from django.urls import resolve, reverse

from pages.views import AboutPageView, HomePageView, PrivacyPageView, SearchPageView, TermsPageView
from places.views import PlaceListView


class HomePageTests(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse('pages:home'))
        no_response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Volu')
        self.assertTemplateUsed(response, 'places/place_list.html')
        self.assertNotContains(response, 'Hi I should not be on this page')
        self.assertEqual(no_response.status_code, 404)

    def test_home_page_resolves_placelistview(self):
        view = resolve(reverse('pages:home'))
        self.assertEqual(view.func.__name__, PlaceListView.as_view().__name__)


class AboutPageTests(TestCase):
    def test_about_page_works(self):
        response = self.client.get(reverse('pages:about'))
        no_response = self.client.get('/about-us/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')
        self.assertTemplateUsed(response, 'pages/about.html')
        self.assertNotContains(response, 'Hi I should not be on this page')
        self.assertEqual(no_response.status_code, 404)

    def test_about_page_resolves_homepageview(self):
        view = resolve(reverse('pages:about'))
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)


class SearchPageTests(TestCase):
    def test_search_page_works(self):
        response = self.client.get(reverse('pages:search'))
        no_response = self.client.get('search-results')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search')
        self.assertTemplateUsed(response, 'pages/search.html')
        self.assertNotContains(response, 'Hi I should not be on this page.')
        self.assertEqual(no_response.status_code, 404)

    def test_search_page_resolves_searchpageview(self):
        view = resolve(reverse('pages:search'))
        self.assertEqual(view.func.__name__, SearchPageView.as_view().__name__)


class PrivacyPageTests(TestCase):
    def test_privacy_page_works(self):
        response = self.client.get(reverse('pages:privacy'))
        no_response = self.client.get('privacy/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Privacy')
        self.assertTemplateUsed(response, 'pages/privacy.html')
        self.assertNotContains(response, 'Hi I should not be on this page.')
        self.assertEqual(no_response.status_code, 404)

    def test_privacy_page_resolves_privacypageview(self):
        view = resolve(reverse('pages:privacy'))
        self.assertEqual(view.func.__name__, PrivacyPageView.as_view().__name__)


class TermsPageTests(TestCase):
    def test_terms_page_works(self):
        response = self.client.get(reverse('pages:terms'))
        no_response = self.client.get('terms/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Terms')
        self.assertTemplateUsed(response, 'pages/terms.html')
        self.assertNotContains(response, 'Hi I should not be on this page.')
        self.assertEqual(no_response.status_code, 404)

    def test_terms_page_resolves_termspageview(self):
        view = resolve(reverse('pages:terms'))
        self.assertEqual(view.func.__name__, TermsPageView.as_view().__name__)
