from django import forms
from dal import autocomplete
from .models import *


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields= "__all__"

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields= "__all__"
        exclude = ["Patient_idPatient"]
