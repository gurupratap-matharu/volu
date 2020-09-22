from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse('home'))
        no_response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home')
        self.assertTemplateUsed(response, 'pages/home.html')
        self.assertNotContains(response, 'Hi I should not be on this page')
        self.assertEqual(no_response.status_code, 404)
