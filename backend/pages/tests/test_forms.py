from django.core import mail
from django.test import TestCase

from pages.forms import ContactForm, FeedbackForm


class TestContactForm(TestCase):
    def setUp(self) -> None:
        self.url = '/contact/'

    def test_valid_contact_form_sends_email(self):
        form = ContactForm({
            'name': 'Veer',
            'email': 'veerplaying@gmail.com',
            'subject': 'Food for thought',
            'message': 'In the darkest of times you will see the brightest of stars',
        })
        self.assertTrue(form.is_valid())

        with self.assertLogs('pages.forms', level='INFO') as cm:
            form.send_mail()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, '[Contact form] Food for thought')
        self.assertGreaterEqual(len(cm.output), 1)

    def test_invalid_contact_form(self):
        form = ContactForm({'message': 'Hi there'})
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        response = self.client.post(self.url, {
            'name': 'A Random Hacker',
            'email': 'xxx',
            'subject': 'Hello',
            'message': 'Hello, World!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', ['Enter a valid email address.'])

    def test_empty_name(self):
        response = self.client.post(self.url, {
            'name': '',
            'email': 'a.random@example.com',
            'subject': 'Hello',
            'message': 'Hello, World!',
        })
        self.assertFormError(response, 'form', 'name', ['This field is required.'])


class FeedbackFormTest(TestCase):
    def test_valid_feedback_form_sends_email(self):
        form = FeedbackForm({
            'name': 'Veer',
            'email': 'veerplaying@gmail.com',
            'message': 'In the darkest of times you will see the brightest of stars',
        })
        self.assertTrue(form.is_valid())

        with self.assertLogs('pages.forms', level='INFO') as cm:
            form.send_mail()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Volu feedback message from Veer')
        self.assertGreaterEqual(len(cm.output), 1)

    def test_invalid_feedback_form(self):
        form = FeedbackForm({'message': 'Hi there'})
        self.assertFalse(form.is_valid())
