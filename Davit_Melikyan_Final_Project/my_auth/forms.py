from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # def clean_email(self):
    #     email = self.cleaned_data['email'].lower()
    #     try:
    #         account = User.objects.get(email=email)
    #
    #     except Exception as e:
    #         return email
    #     raise forms.ValidationError(f'E-Mail {email} Is Already Exists.')
    #
    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     try:
    #         account = User.objects.get(username=username)
    #
    #     except Exception as e:
    #         return username
    #     raise forms.ValidationError(f'Username {username} Is Already Exists.')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')