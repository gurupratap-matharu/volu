import logging

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class EmailPlaceForm(forms.Form):
    name = forms.CharField(label=_('Your name'), max_length=25)
    email = forms.EmailField(label=_('Your email'))
    to = forms.EmailField(label=_('Recipients email'))
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def send_email(self):
        logger.info('sending place share email...')

        subject = '{0} shares with you'.format(self.cleaned_data['name'])
        message = "{}\'s comments: {}".format(self.cleaned_data['name'], self.cleaned_data['comments'])
        send_mail(subject=subject,
                  message=message,
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[self.cleaned_data['to']],
                  fail_silently=False)
