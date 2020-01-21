from django import forms
from dal import autocomplete
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields= "__all__"