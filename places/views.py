from django.views.generic import DetailView, ListView

from places.models import Place


class PlaceListView(ListView):
    model = Place
    context_object_name = 'place_list'
    template_name = 'places/place_list.html'


class PlaceDetailView(DetailView):
    model = Place
    context_object_name = 'place'
    template_name = 'places/place_detail.html'
