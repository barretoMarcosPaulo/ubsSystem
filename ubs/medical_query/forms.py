from django import forms
from dal import autocomplete
from .models import *

class MedicalQueryForm(forms.ModelForm):
    class Meta:
        model = MedicalQuery
        fields= "__all__"

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields= "__all__"

