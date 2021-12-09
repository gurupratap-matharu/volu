import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

import stripe

logger = logging.getLogger(__name__)

CustomUser = get_user_model()


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/purchase.html'


class PaymentSuccessfulView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/payment_success.html'


class PaymentCancelledView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/payment_cancel.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        logger.info('generating stripe config...')
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        logger.info('creating stripe checkout session...')

        client_reference_id = request.user.id if request.user.is_authenticated else None
        stripe.api_key = settings.STRIPE_SECRET_KEY

        domain_url = request.build_absolute_uri(reverse('orders:home'))
        success_url = domain_url + 'success?session_id={CHECKOUT_SESSION_ID}'
        cancel_url = domain_url + 'cancelled/'

        logger.info("domain url to: %s" % domain_url)
        logger.info("success url to: %s" % success_url)
        logger.info("cancel url to: %s" % cancel_url)

        line_items = [{
            'name': 'Pro Membership',
            'quantity': 1,
            'currency': 'usd',
            'amount': '8900',
        }]

        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=client_reference_id,
                success_url=success_url,
                cancel_url=cancel_url,
                payment_method_types=['card'],
                mode='payment',
                line_items=line_items
            )

            session_id = checkout_session['id']

            return JsonResponse({'sessionId': session_id})

        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
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

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        logger.info('Payment was successful.')

        # Fetch all the required data from the session
        client_reference_id = session.get('client_reference_id')
        # get our user who paid money
        user = CustomUser.objects.get(id=client_reference_id)
        # Todo.
        # Do something here as user has paid
        # like set permissions, make user pro member, etc
        # we are not saving the stripe details in our database in one time payments

    return HttpResponse(status=200)
