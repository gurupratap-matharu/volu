import logging

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.http.response import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

import stripe

logger = logging.getLogger(__name__)


class SubscriptionPageView(LoginRequiredMixin, TemplateView):
    template_name = 'subscriptions/purchase.html'


class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'subscriptions/payment_success.html'


class PaymentCancelView(LoginRequiredMixin, TemplateView):
    template_name = 'subscriptions/payment_cancel.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        logger.info('sending stripe config...')
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        logger.info('creating stripe checkout session...')

        stripe.api_key = settings.STRIPE_SECRET_KEY
        client_reference_id = request.user.id if request.user.is_authenticated else None

        domain_url = request.build_absolute_uri(reverse('subscriptions'))
        success_url = domain_url + 'success?session_id={CHECKOUT_SESSION_ID}'
        cancel_url = domain_url + 'cancel/'

        logger.debug("domain url to: %s" % domain_url)
        logger.debug("success url to: %s" % success_url)
        logger.debug("cancel url to: %s" % cancel_url)

        line_items = [{'price': settings.STRIPE_PRICE_ID, 'quantity': 1}]
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=client_reference_id,
                success_url=success_url,
                cancel_url=cancel_url,
                payment_method_types=['card'],
                mode='subscription',
                line_items=line_items
            )

            session_id = checkout_session['id']

            return JsonResponse({'sessionId': session_id})

        except Exception as e:
            return JsonResponse({'error': str(e)})
