from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, TemplateView

from pages.forms import ContactForm, FeedbackForm, SearchForm


class HomePageView(FormView):
    form_class = SearchForm
    template_name = 'pages/home.html'


class LoginPageView(TemplateView):
    template_name = 'pages/login.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


class ContactPageView(SuccessMessageMixin, FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_message = 'Message received successfully!'
    success_url = '/'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class FeedbackPageView(SuccessMessageMixin, FormView):
    template_name = 'pages/feedback.html'
    form_class = FeedbackForm
    success_message = 'Feedback received successfully!'
    success_url = '/'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)
