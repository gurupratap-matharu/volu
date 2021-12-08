from django.urls import path

from .views import (
    PaymentCancelView, PaymentSuccessView, SubscriptionPageView, create_checkout_session,
    stripe_config, stripe_webhook,
)

urlpatterns = [
    path('', SubscriptionPageView.as_view(), name='subscriptions'),
    path('config/', stripe_config, name='stripe-config'),
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
]
