from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):

    ROLE_CHOICES = [
        ('User', 'User'),
        ('Author', 'Author'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'password1',
            'password2'
        )