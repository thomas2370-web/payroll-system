from django.contrib.auth.forms import AuthenticationForm
from django.forms import TextInput, PasswordInput


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = TextInput(attrs={"class": "form-control"})
        self.fields["password"].widget = PasswordInput(attrs={"class": "form-control"})
