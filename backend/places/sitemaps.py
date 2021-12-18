from django.contrib.sitemaps import Sitemap

from .models import Place


class PlaceSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Place.listed.all()

    def lastmod(self, obj):
        return obj.updated_on
