from django.shortcuts import render
# Create your views here.
from .forms import PatientForm,MedicalQueryForm
from .models import Patient,MedicalQuery

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

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
    return render(request, 'patient/new_patient.html')


class QueryCreate(CreateView):
	model = MedicalQuery
	template_name = 'querys/add.html'
	form_class = MedicalQueryForm

	# def form_valid(self, form):
	# 	form.save()
	# 	messages.success(self.request, 'Vivência cadastrada com sucesso.')
	# 	return HttpResponseRedirect(self.get_success_url())

	# def form_invalid(self, form):
	# 	messages.error(self.request, 'Ocorreu um erro ao cadastrar a vivência.')
	# 	return self.render_to_response(
	# 		self.get_context_data(
	# 			form=form
	# 		)
	# 	)

	# def get_success_url(self):
	# 	return reverse('nucleo:vivencia_list')