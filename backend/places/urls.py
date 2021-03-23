from django.urls import path

from places.views import (PlaceCreate, PlaceDelete, PlaceDetailView,
                          PlaceListView, PlaceUpdate)

app_name = 'places'

urlpatterns = [
    path('', PlaceListView.as_view(), name='place_list'),
    path('<uuid:pk>/', PlaceDetailView.as_view(), name='place_detail'),
    path('create/', PlaceCreate.as_view(), name='place_create'),
    path('<uuid:pk>/update/', PlaceUpdate.as_view(), name='place_update'),
    path('<uuid:pk>/delete/', PlaceDelete.as_view(), name='place_delete'),
]
