import logging

from django import forms
from django.core.mail import send_mail

from .models import Comment

logger = logging.getLogger(__name__)


class PostShareForm(forms.Form):
    name = forms.CharField(max_length=25, label='Your name')
    email = forms.EmailField(label='Your email')
    to = forms.EmailField(label="Recipient's email")
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def send_mail(self, post=None):
        logger.info('sending post share email...')

        subject = '{0} recommends you read {1}'.format(self.cleaned_data['name'], post.title)
        message = "Read {} at {}\n\n{}\'s comments: {}".format(post.title, post.url,
                                                               self.cleaned_data['name'],
                                                               self.cleaned_data['comments'])
        send_mail(subject=subject, message=message,
                  from_email='admin@site.domain',
                  recipient_list=[self.cleaned_data['to']], fail_silently=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
