from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from dal import autocomplete
from .models import *



class UserAdminForm(UserCreationForm):
    class Meta:
        model = User
        fields= ['full_name','cpf','email','phone']



class UserClerkForm(UserCreationForm):
    class Meta:
        model = Clerk
        fields= ['full_name','cpf','register_clerk','email','phone']



class UserDoctorForm(UserCreationForm):
    class Meta:
        model = Doctor
        fields= "__all__"


