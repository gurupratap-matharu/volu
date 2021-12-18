from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from blog.sitemaps import PostSitemap
from places.sitemaps import PlaceSiteMap

sitemaps = {
    'posts': PostSitemap,
    'places': PlaceSiteMap,
}

urlpatterns = [
    # Django administration
    path('dj-admin/', admin.site.urls),

    # User management
    path('accounts/', include('allauth.urls')),

    # Translation
    path('rosetta/', include('rosetta.urls')),

    # Local apps
    path('', include('pages.urls', namespace='pages')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('places/', include('places.urls', namespace='places')),
    path('profile/', include('users.urls', namespace='users')),
    path('orders/', include('orders.urls')),
    path('subscriptions/', include('subscriptions.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
