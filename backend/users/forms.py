from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import LudoUser

class LudoUserCreationForm(UserCreationForm):
    class Meta:
        model = LudoUser
        fields = ('username', 'email')

class LudoUserChangeForm(UserChangeForm):
    class Meta:
        model = LudoUser
        fields = ('username', 'email')
        