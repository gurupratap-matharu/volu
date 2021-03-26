from django.urls import path

from places.views import (PlaceCreate, PlaceDelete, PlaceDetailView,
                          PlaceListView, PlaceUpdate)

app_name = 'places'

urlpatterns = [
    path('', PlaceListView.as_view(), name='place_list'),
    path('create/', PlaceCreate.as_view(), name='place_create'),
    path('<int:year>/<int:month>/<int:day>/<slug:place>/', PlaceDetailView.as_view(), name='place_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:place>/update/', PlaceUpdate.as_view(), name='place_update'),
    path('<int:year>/<int:month>/<int:day>/<slug:place>/delete/', PlaceDelete.as_view(), name='place_delete'),
]
