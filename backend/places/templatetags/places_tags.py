from django import template
from places.models import Place

register = template.Library()


@register.simple_tag
def total_places():
    return Place.objects.count()
