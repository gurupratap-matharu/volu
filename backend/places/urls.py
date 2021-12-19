from django.urls import path

from places.views import (
    PlaceCreate, PlaceDelete, PlaceDetailView, PlaceListView, PlaceShareView, PlaceUpdate,
    SearchResultsView,
)

from .feeds import LatestPlacesFeed

app_name = 'places'

urlpatterns = [
    path('', PlaceListView.as_view(), name='place_list'),
    path('tag/<slug:tag_slug>/', PlaceListView.as_view(), name='place_list_by_tag'),
    path('create/', PlaceCreate.as_view(), name='place_create'),
    path('<uuid:pk>/', PlaceDetailView.as_view(), name='place_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:place>/update/', PlaceUpdate.as_view(), name='place_update'),
    path('<int:year>/<int:month>/<int:day>/<slug:place>/delete/', PlaceDelete.as_view(), name='place_delete'),
    path('share/', PlaceShareView.as_view(), name='place_share'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('feed/', LatestPlacesFeed(), name='place_feed')

]
