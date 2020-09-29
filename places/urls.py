from django.urls import path

from places.views import PlaceDetailView, PlaceListView

urlpatterns = [
    path('', PlaceListView.as_view(), name='place_list'),
    path('<uuid:pk>/', PlaceDetailView.as_view(), name='place_detail'),
]
