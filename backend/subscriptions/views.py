import logging
from typing import Any, Dict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

import stripe

from .models import StripeCustomer

logger = logging.getLogger(__name__)

CustomUser = get_user_model()


class SubscriptionPageView(LoginRequiredMixin, TemplateView):
    template_name = 'subscriptions/purchase.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        try:
            # Retrieve the subscription & product
            stripe_customer = StripeCustomer.objects.get(user=self.request.user)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            subscription = stripe.Subscription.retrieve(stripe_customer.stripe_subscription_id)
            product = stripe.Product.retrieve(subscription.plan.product)

            # Feel free to fetch any additional data from 'subscription' or 'product'
            # https://stripe.com/docs/api/subscriptions/object
            # https://stripe.com/docs/api/products/object

            logger.info('%s has a valid subscription' % self.request.user)
            context['subscription'] = subscription
            context['product'] = product

        except StripeCustomer.DoesNotExist:
            logger.info("%s has no valid subscription." % self.request.user)
            pass

        return context


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


@csrf_exempt
def stripe_webhook(request):
    logger.info('got ping from stripe...')

    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from the session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new StripeCustomer
        user = CustomUser.objects.get(id=client_reference_id)
        StripeCustomer.objects.create(
            user=user,
            stripe_customer_id=stripe_customer_id,
            stripe_subscription_id=stripe_subscription_id,
        )

        logger.info(user.email + ' just subscribed!!! :D')

    return HttpResponse(status=200)
