import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django_countries.fields import CountryField


class CustomUser(AbstractUser):
    pass


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.CharField(max_length=600, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    country = CountryField(blank_label='(select country)')
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')

    def get_absolute_url(self):
        return reverse('users:profile_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('users:profile_update', args=[str(self.id)])

    def can_update(self, user):
        return user.is_superuser or self.user == user


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
