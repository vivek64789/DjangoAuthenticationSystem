from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    username = forms.CharField(
        widget=forms.TextInput(attrs={"type": "text", "class": "form-control", "placeholder":"Enter Username...",}),
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"type": "text", "class": "form-control", "placeholder":"Enter Username...",}),)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"type": "text", "class": "form-control", "placeholder":"Enter Username...",}),
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={"type": "email", "class": "form-control","placeholder":"Enter Email Address...",}),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"type": "password", "class": "form-control","placeholder":"Enter Password...",}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"type": "password", "class": "form-control","placeholder":"Confirm Password...",}),
    )
