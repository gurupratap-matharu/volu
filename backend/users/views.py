import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.views.generic import DetailView, UpdateView

from users.forms import ProfileUpdateForm
from users.models import Profile

logger = logging.getLogger(__name__)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'


class ProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'users/profile_update_form.html'
    success_message = 'Profile successfully updated!'

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.can_update(self.request.user):
            logger.warning('Possible attack: \nuser: %s\nobj: %s', self.request.user, obj)
            raise Http404
        return obj
