from places.views import (
    PlaceCreate, PlaceDelete, PlaceDetailView, PlaceListView, PlaceUpdate,
)

from django.urls import path

app_name = 'places'

urlpatterns = [
    path('', PlaceListView.as_view(), name='place_list'),
    path('tag/<slug:tag_slug>/', PlaceListView.as_view(), name='place_list_by_tag'),
    path('create/', PlaceCreate.as_view(), name='place_create'),
    path('<uuid:pk>/', PlaceDetailView.as_view(), name='place_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:place>/update/', PlaceUpdate.as_view(), name='place_update'),
    path('<int:year>/<int:month>/<int:day>/<slug:place>/delete/', PlaceDelete.as_view(), name='place_delete'),
]
