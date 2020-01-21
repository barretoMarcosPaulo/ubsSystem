from django import forms
from dal import autocomplete
from .models import *

class MedicalQueryForm(forms.ModelForm):
    class Meta:
        model = MedicalQuery
        fields= "__all__"
