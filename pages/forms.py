import logging

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

logger = logging.getLogger(__name__)


class SearchForm(forms.Form):
    country = CountryField().formfield(widget=CountrySelectWidget(),
                                       layout='{widget}<img class="country-select-flag" id="{flag_id}" style="margin: 6px 4px 0" src="{country.flag}">'
                                       )


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Message', max_length=600, widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))

    def send_mail(self):
        logger.info('Sending email...')
        message = 'From: {0}\n{1}\n{2}'.format(
            self.cleaned_data['name'],
            self.cleaned_data['email'],
            self.cleaned_data['message']
        )
        logger.info('message: %s', message)
        send_mail(subject='Site message',
                  message=message,
                  from_email='site@website.domain',
                  recipient_list=settings.RECIPIENT_LIST,
                  fail_silently=False)


class FeedbackForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Feedback', max_length=400, widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))

    def send_mail(self):
        logger.info('Sending feedback...')
        message = 'From: {0}\n{1}\n{2}'.format(
            self.cleaned_data['name'], self.cleaned_data['email'], self.cleaned_data['message'])
        logger.info('message: %s', message)
        send_mail(subject='Feedback message',
                  message=message,
                  from_email=self.cleaned_data['email'],
                  recipient_list=settings.RECIPIENT_LIST,
                  fail_silently=False)
