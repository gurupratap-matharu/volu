from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, TemplateView

from pages import forms


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class LoginPageView(TemplateView):
    template_name = 'pages/login.html'


class ProfilePageView(TemplateView):
    template_name = 'pages/profile.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


class ContactPageView(SuccessMessageMixin, FormView):
    template_name = 'pages/contact.html'
    form_class = forms.ContactForm
    success_message = 'Message received successfully!'
    success_url = '/'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class FeedbackPageView(SuccessMessageMixin, FormView):
    template_name = 'pages/feedback.html'
    form_class = forms.FeedbackForm
    success_message = 'Feedback received successfully!'
    success_url = '/'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)
