from django.urls import path

from .views import (
    HomePageView, PaymentCancelledView, PaymentSuccessfulView, create_checkout_session,
    stripe_config, stripe_webhook,
)

app_name = 'orders'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('success/', PaymentSuccessfulView.as_view(), name='payment-success'),
    path('cancelled/', PaymentCancelledView.as_view(), name='payment-cancelled'),
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('config/', stripe_config, name='config'),
    path('webhook/', stripe_webhook, name='webhook'),
]
