from django import forms
from dal import autocomplete
from .models import *


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields= "__all__"
