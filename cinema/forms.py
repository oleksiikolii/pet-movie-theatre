from django import forms
from django.contrib.auth.forms import UserCreationForm

from cinema.models import Guest


class GuestCreationForm(UserCreationForm):
    class Meta:
        model = Guest
        fields = UserCreationForm.Meta.fields  # + ("email",)


class MovieSearchForm(forms.Form):
    title = forms.CharField(max_length=100, label="")
