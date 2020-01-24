from django.shortcuts import render
# Create your views here.
from .forms import PatientForm

def new_patient(request):
    form = PatientForm()
    return render(request, 'medical_query/new_patient.html', {'form': form})