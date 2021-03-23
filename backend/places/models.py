import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField


class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    email = models.EmailField()

    address1 = models.CharField('Address line 1', max_length=60)
    address2 = models.CharField('Address line 2', max_length=60)
    zip_code = models.CharField('ZIP / Postal Code', max_length=12)
    city = models.CharField(max_length=60)
    country = CountryField(blank_label='(select country)')

    is_active = models.BooleanField(default=True)
    ratings = models.PositiveIntegerField(default=0)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    host = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='places')

    class Meta:
        ordering = ['-updated_on']

    def __str__(self):
        return ", ".join([self.name, self.country.name])

    def get_absolute_url(self):
        return reverse('places:place_detail', args=[str(self.id)])

    def can_update(self, user):
        return user.is_superuser or self.host == user

    def can_delete(self, user):
        return user.is_superuser or self.host == user
