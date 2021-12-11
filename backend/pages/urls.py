from django.urls import path

from pages.views import (
    AboutPageView, ContactPageView, FeedbackPageView, HomePageView, SearchPageView,
)

app_name = 'pages'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('feedback/', FeedbackPageView.as_view(), name='feedback'),
    path('search/', SearchPageView.as_view(), name='search'),
]
