from django.test import TestCase
from django.urls import resolve
from users.factories import superuser_factory, user_factory
from users.views import ProfileDetailView, ProfileUpdate


class ProfileDetailTests(TestCase):
    def setUp(self):
        self.user = user_factory()

    def test_profile_detail_resolves_profiledetailview(self):
        view = resolve(self.user.profile.get_absolute_url())
        self.assertEqual(view.func.__name__, ProfileDetailView.as_view().__name__)

    def test_profile_detail_redirects_for_anonymous_user(self):
        response = self.client.get(self.user.profile.get_absolute_url())
        no_response = self.client.get('/profile/')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'users/profile_detail.html')
        self.assertEqual(no_response.status_code, 404)

    def test_profile_detail_works_for_logged_in_user(self):
        self.client.force_login(self.user)

        response = self.client.get(self.user.profile.get_absolute_url())
        no_response = self.client.get('/profile/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_detail.html')
        self.assertContains(response, 'Profile')
        self.assertContains(response, self.user.profile.bio)
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)


class ProfileUpdateTests(TestCase):
    def setUp(self):
        self.superuser = superuser_factory()
        self.user = user_factory()
        self.bad_user = user_factory()

    def test_profile_update_resolves_profileupdateview(self):
        view = resolve(self.user.profile.get_update_url())
        self.assertEqual(view.func.__name__, ProfileUpdate.as_view().__name__)

    def test_profile_update_redirects_for_anonymous_user(self):
        response = self.client.get(self.user.profile.get_update_url())
        no_response = self.client.get('/profile/update/')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'users/profile_update_form.html')
        self.assertEqual(no_response.status_code, 404)

    def test_profile_update_works_for_logged_in_user(self):
        self.client.force_login(self.user)

        response = self.client.get(self.user.profile.get_update_url())
        no_response = self.client.get('/profile/update/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_update_form.html')
        self.assertContains(response, 'Update')
        self.assertContains(response, self.user.profile.bio)
        self.assertNotContains(response, 'Hi I should not be on this page!')
        self.assertEqual(no_response.status_code, 404)

    def test_profile_update_with_valid_data_on_post_works(self):
        self.client.force_login(self.user)
        data = {'country': 'Argentina', 'bio': 'Backpacking across the globe', 'birth_date': '03-07-1985'}

        response = self.client.post(self.user.profile.get_update_url(), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'users/profile_detail.html')
        self.assertEqual(self.user.profile.bio, 'Backpacking across the globe')
        self.assertEqual(self.user.profile.country.code, 'AR')
        self.assertEqual(self.user.profile.birth_date, '1985-07-03')

    def test_a_user_cannot_update_another_users_profile(self):
        self.client.force_login(self.bad_user)
        data = {'country': 'Argentina', 'bio': 'Backpacking across the globe', 'birth_date': '03-07-1985'}

        response = self.client.post(self.user.profile.get_update_url(), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'users/profile_detail.html')
        self.assertEqual(self.user.profile.bio, 'Backpacking across the globe')
        self.assertEqual(self.user.profile.country.code, 'AR')
        self.assertEqual(self.user.profile.birth_date, '1985-07-03')
