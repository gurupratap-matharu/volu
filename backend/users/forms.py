from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'birth_date', 'country',)
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'birth_date': forms.DateInput(
                format=('%m-%d-%Y'), attrs={'class': 'datetimepicker', 'type': 'text'})
        }
