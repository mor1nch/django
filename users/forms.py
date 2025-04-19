from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'country']


# accounts/forms.py

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label='Введите ваш email', max_length=254)
