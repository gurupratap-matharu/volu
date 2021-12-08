from django.contrib.auth import get_user_model
from django.db import models


class StripeCustomer(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return self.user.email
