import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from places.models import Place

logger = logging.getLogger(__name__)


class PlaceListView(ListView):
    model = Place
    context_object_name = 'place_list'
    paginate_by = 6
    template_name = 'places/place_list.html'


class PlaceDetailView(DetailView):
    model = Place
    context_object_name = 'place'
    template_name = 'places/place_detail.html'


class PlaceCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Place
    fields = ['name', 'description', 'email', 'address1', 'address2', 'zip_code', 'city', 'country', 'is_active']
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
        obj = super().get_object()
        if not obj.can_update(self.request.user):
            logger.warning('Possible attack: \nuser: %s\nobj: %s', self.request.user, obj)
            raise Http404
        return obj


class PlaceDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Place
    success_url = reverse_lazy('home')
    success_message = "Place deleted successfully!"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.can_delete(self.request.user):
            logger.warning('Possible attack: \nuser: %s\nobj: %s', self.request.user, obj)
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PlaceDelete, self).delete(request, *args, **kwargs)
