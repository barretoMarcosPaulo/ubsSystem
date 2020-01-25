from django import forms
from dal import autocomplete
from .models import *

class MedicalQueryForm(forms.ModelForm):
    class Meta:
        model = MedicalQuery
        exclude = ['medical','date']
        fields= "__all__"

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields= "__all__"

class PhysicalExamForm(forms.ModelForm):
    class Meta:
        model = PhysicalExam
        exclude = ['query']
        fields= "__all__"