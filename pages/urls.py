from django.urls import path

from pages.views import (AboutPageView, ContactPageView, FeedbackPageView,
                         HomePageView, LoginPageView, ProfilePageView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('feedback/', FeedbackPageView.as_view(), name='feedback'),
]
