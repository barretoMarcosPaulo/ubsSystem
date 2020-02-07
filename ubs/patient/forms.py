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

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields= "__all__"

class CityDetailForm(forms.ModelForm):
    State_codIBGE_UF = forms.CharField(label='Estado')
    def __init__(self, *args, **kwargs):
        super(CityDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields: 
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = City
        fields= "__all__"

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields= "__all__"