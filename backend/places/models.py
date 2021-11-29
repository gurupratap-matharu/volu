import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from .utils import place_image_path, place_thumbnail_path


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique_for_date='created_on')
    description = models.TextField()
    email = models.EmailField()
    address1 = models.CharField('Address line 1', max_length=200)
    address2 = models.CharField('Address line 2', max_length=200)
    zip_code = models.CharField('ZIP / Postal Code', max_length=12)
    city = models.CharField(max_length=60)
    country = CountryField(blank_label='(select country)')

    is_active = models.BooleanField(default=True)
    ratings = models.PositiveIntegerField(default=0)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    host = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='places')

    class Meta:
        ordering = ('-updated_on',)

    objects = models.Manager()
    tags = TaggableManager(through=UUIDTaggedItem)

    def __str__(self):
        return ", ".join([self.name, self.country.name])

    def get_absolute_url(self):
        return reverse('places:place_detail', args=[self.id])

    def get_share_url(self):
        return self.get_absolute_url() + 'share/'

    def get_comment_url(self):
        return self.get_absolute_url() + 'comment/'

    def can_update(self, user):
        return user.is_superuser or self.host == user

    def can_delete(self, user):
        return user.is_superuser or self.host == user


class PlaceImage(models.Model):
    place = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=place_image_path)
    thumbnail = models.ImageField(upload_to=place_thumbnail_path, null=True)

    def __str__(self):
        return ", ".join([self.image.url, str(self.place)])
