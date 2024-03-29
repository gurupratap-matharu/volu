from django.urls import path

from pages.views import (
    AboutPageView, ContactPageView, FeedbackPageView, PrivacyPageView, SearchPageView,
    TermsPageView,
)
from places.views import PlaceListView

app_name = 'pages'

urlpatterns = [
    path('', PlaceListView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('feedback/', FeedbackPageView.as_view(), name='feedback'),
    path('search/', SearchPageView.as_view(), name='search'),
    path('privacy/', PrivacyPageView.as_view(), name='privacy'),
    path('terms/', TermsPageView.as_view(), name='terms'),
]
