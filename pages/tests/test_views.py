from django.test import TestCase
from django.urls import resolve, reverse

from pages.views import AboutPageView, HomePageView, LoginPageView


class HomePageTests(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse('home'))
        no_response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home')
        self.assertTemplateUsed(response, 'pages/home.html')
        self.assertNotContains(response, 'Hi I should not be on this page')
        self.assertEqual(no_response.status_code, 404)

    def test_home_page_resolves_homepageview(self):
        view = resolve(reverse('home'))
        self.assertEqual(view.__name__, HomePageView.as_view().__name__)


class AboutPageTests(TestCase):
    def test_about_page_works(self):
        response = self.client.get(reverse('about'))
        no_response = self.client.get('/about-us/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')
        self.assertTemplateUsed(response, 'pages/about.html')
        self.assertNotContains(response, 'Hi I should not be on this page')
        self.assertEqual(no_response.status_code, 404)

    def test_about_page_resolves_homepageview(self):
        view = resolve(reverse('about'))
        self.assertEqual(view.__name__, AboutPageView.as_view().__name__)
