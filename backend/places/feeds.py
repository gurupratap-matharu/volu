from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy

from .models import Place


class LatestPlacesFeed(Feed):
    title = 'Volunteering Opportunities'
    link = reverse_lazy('places:place_list')
    description = 'New volunteering opportunities from VoluHunt'

    def items(self):
        return Place.listed.all()[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return truncatewords(item.description, 30)
