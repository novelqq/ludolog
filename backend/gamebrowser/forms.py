from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Log
import requests
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LogForm(ModelForm):
    class Meta:
        model = Log
        fields = ('score', 'review', 'status')

class SearchForm(forms.Form):
    game_name = forms.CharField(label='Game Name', max_length=100)
    # platform_choices = requests.post('https://api-v3.igdb.com/platforms',
    #         data='fields name; limit 60', 
    #         headers={'user-key': '03093c78ab27aa2fb5752d2b7b9167e4'})
    # PLATFORM_CHOICES = ()
    
