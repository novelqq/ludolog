from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import LudoUserChangeForm, LudoUserCreationForm
from .models import LudoUser

class LudoUserAdmin(UserAdmin):
    add_form = LudoUserCreationForm
    form = LudoUserChangeForm
    model = LudoUser
    list_display = ['email', 'password']
    
admin.site.register(LudoUser, LudoUserAdmin)
