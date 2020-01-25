from django.shortcuts import render
# Create your views here.
from .forms import PatientForm
from .models import Patient

def new_patient(request):
    if request.POST:
        full_name = request.POST['full_name']
        date_birth = request.POST['date_birth']
        sex = request.POST['sex']
        color = request.POST['color']
        marital_state = request.POST['marital_state']
        ocupation = request.POST['ocupation']
        local_birth = request.POST['local_birth']
        health_insurance = request.POST['health_insurance']
        address = request.POST['address']
        phone = request.POST['phone']
        fax = request.POST['fax']
        email = request.POST['email']
        patient = Patient.objects.create(full_name=full_name, date_birth=date_birth, sex=sex,color=color, marital_state=marital_state, ocupation=ocupation, local_birth=local_birth, health_insurance=health_insurance, address=address, phone=phone, fax=fax, email=email )
        patient.save()
        # return HttpResponseRedirect(reverse('partner:index'))
    return render(request, 'medical_query/new_patient.html')