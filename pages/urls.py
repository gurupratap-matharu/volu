from django.urls import path

from pages.views import (AboutPageView, HomePageView, LoginPageView,
                         ProfilePageView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('about/', AboutPageView.as_view(), name='about'),
]
