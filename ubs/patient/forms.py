from django import forms
from dal import autocomplete
from .models import *
from django.forms import inlineformset_factory


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields= "__all__"

class PatientDetailForm(forms.ModelForm):
    # Type_Logradouro_idLogradouro = forms.CharField(label='Logradouro')
    City_codIBGE = forms.CharField(label='Cidade')
    # Color_idColor = forms.CharField(label='Cor')
    # Marital_State_idMarital_State = forms.CharField(label='Estado Conjugal')
    # Ocupation_idOcupation = forms.CharField(label='Ocupação')
    # Medical_Insurance_idMedical_insurance = forms.CharField(label='Convênio')
    def __init__(self, *args, **kwargs):
        super(PatientDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields: 
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = Patient
        fields= "__all__"

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields= "__all__"
        exclude = ["Patient_idPatient"]
PhoneFormset = inlineformset_factory(Patient,Phone,form=PhoneForm)    

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields= "__all__"

class CityEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CityEditForm, self).__init__(*args, **kwargs)
        self.fields['codIBGE'].widget.attrs['readonly'] = True

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

class StateEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StateEditForm, self).__init__(*args, **kwargs)
        self.fields['codIBGE_UF'].widget.attrs['readonly'] = True

    class Meta:
        model = State
        fields= "__all__"

class StateDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StateDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields: 
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = State
        fields= "__all__"

class MedicalInsuranceForm(forms.ModelForm):
    class Meta:
        model = MedicalInsurance
        fields= "__all__"

class MedicalInsuranceDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MedicalInsuranceDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields: 
            self.fields[field].widget.attrs['readonly'] = True
    class Meta:
        model = MedicalInsurance
        fields= "__all__"

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields= "__all__"

class ColorDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ColorDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields: 
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = Color
        fields= "__all__"

class MaritalStateForm(forms.ModelForm):
    class Meta:
        model = MaritalState
        fields= "__all__"

class MaritalStateDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MaritalStateDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields: 
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = MaritalState
        fields= "__all__"

class TypeLogradouroForm(forms.ModelForm):
    class Meta:
        model = TypeLogradouro
        fields= "__all__"

class TypeLogradouroDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TypeLogradouroDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields: 
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = TypeLogradouro
        fields= "__all__"

class OcupationForm(forms.ModelForm):
    class Meta:
        model = Ocupation
        fields= "__all__"

class OcupationDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OcupationDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields: 
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = Ocupation
        fields= "__all__"

class PhoneFormAdmin(forms.ModelForm):
    class Meta:
        model = Phone
        fields= "__all__"

class PhoneDetailForm(forms.ModelForm):
    Patient_idPatient = forms.CharField(label='Paciente')
    def __init__(self, *args, **kwargs):
        super(PhoneDetailForm, self).__init__(*args, **kwargs)
        for field in self.fields: 
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = Phone
        fields= "__all__"