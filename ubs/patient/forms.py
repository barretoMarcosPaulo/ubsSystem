from django import forms
from dal import autocomplete
from .models import *


class PatientForm(forms.ModelForm):
    # date_birth = forms.DateField(widget=forms.TextInput(attrs={'type' : 'date',}), label="Data de nascimento")
    class Meta:
        model = Patient
        fields= "__all__"

class PhoneForm(forms.ModelForm):
    # phone_number = forms.CharField(widget=forms.TextInput(attrs={'maxlength' : '13','onkeypress' : 'return event.charCode >= 48 && event.charCode <= 57',}),label="Número de telefone")
    class Meta:
        model = Phone
        fields= "__all__"
