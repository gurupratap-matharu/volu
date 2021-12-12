from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, TemplateView

from pages.forms import ContactForm, FeedbackForm


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


class ContactPageView(SuccessMessageMixin, FormView):
    form_class = ContactForm
    template_name = 'pages/contact.html'
    success_message = 'Message received successfully!'
    success_url = '/'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class FeedbackPageView(SuccessMessageMixin, FormView):
    form_class = FeedbackForm
    template_name = 'pages/feedback.html'
    success_message = 'Feedback received successfully!'
    success_url = '/'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class SearchPageView(TemplateView):
    template_name = 'pages/search.html'
