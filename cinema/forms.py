from django.contrib.auth.forms import UserCreationForm

from cinema.models import Guest


class GuestCreationForm(UserCreationForm):
    class Meta:
        model = Guest
        fields = UserCreationForm.Meta.fields #+ ("email",)
