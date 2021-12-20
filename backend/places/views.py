import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q, QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import FormView

from taggit.models import Tag

from .forms import EmailPlaceForm
from .models import Place

logger = logging.getLogger(__name__)


class PlaceListView(ListView):
    model = Place
    context_object_name = 'place_list'
    paginate_by = 9
    template_name = 'places/place_list.html'

    def get_queryset(self):
        queryset = Place.listed.all()
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            self.extra_context = {'tag': tag}
            queryset = queryset.filter(tags__in=[tag])
        return queryset


class PlaceDetailView(DetailView):
    model = Place
    context_object_name = 'place'
    template_name = 'places/place_detail.html'


class PlaceCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Place
    fields = [
        'name', 'description', 'email', 'address1', 'address2', 'zip_code',
        'city', 'country', 'is_active'
    ]
    sucess_message = "%(name)s successfully created!"

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)


class PlaceUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Place
    fields = ['name', 'description', 'email', 'address1', 'address2', 'zip_code', 'is_active']
    sucess_message = "%(name)s successfully updated!"
    template_name = 'places/place_update_form.html'

    def get_object(self, queryset=None):
        obj = self.obj
        if not obj.can_update(self.request.user):
            logger.warning('Possible attack: \nuser: %s\nobj: %s',
                           self.request.user, obj)
            raise Http404
        return obj


class PlaceDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Place
    success_url = reverse_lazy('pages:home')
    success_message = "Place deleted successfully!"

    def get_object(self, queryset=None):
        obj = self.obj
        if not obj.can_delete(self.request.user):
            logger.warning('Possible attack: \nuser: %s\nobj: %s',
                           self.request.user, obj)
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PlaceDelete, self).delete(request, *args, **kwargs)


class PlaceShareView(FormView):
    form_class = EmailPlaceForm
    template_name = 'places/place_share_form.html'
    success_url = reverse_lazy('places:place_list')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class SearchResultsView(ListView):
    model = Place
    template_name = 'places/search_results.html'
    context_object_name = 'place_list'
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get("q")
        search_vector = SearchVector('name', 'description')
        search_query = SearchQuery(query)

        return (
            Place.listed.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(search=search_query)
            .order_by('-rank')
        )
