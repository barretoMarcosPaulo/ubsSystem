from django.shortcuts import render
# Create your views here.
from .forms import PatientForm,MedicalQueryForm,PhysicalExamForm
from .models import Patient,MedicalQuery,PhysicalExam

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.db import IntegrityError, transaction


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
    second_form_class = PhysicalExamForm

    def get(self, request, *args, **kwargs):
        
        print(MedicalQuery.objects.all())
        print(PhysicalExam.objects.all())

        self.object = None
        form = self.form_class
        exam_form = self.second_form_class
        return self.render_to_response(
            self.get_context_data(
                form=form,
                exam_form=exam_form,
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST, self.request.FILES)
        exam_form = self.second_form_class(self.request.POST)
        if form.is_valid() and exam_form.is_valid():
            return self.form_valid(form, exam_form)
        else:
            return self.form_invalid(form, exam_form)

    def form_valid(self, form, exam_form):
       
        with transaction.atomic():
            print("OK")

            query = form.save(commit=False)
            # query.medical = self.request.user
            query.save()

            exam = exam_form.save(commit=False)
            exam.query = query
            exam.save()

            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, exam_form):
        print("Formulario Invalido")
        return self.render_to_response(
            self.get_context_data(
                    form=form,
                    exam_form=exam_form,
                )
            )

    def get_success_url(self):
        return reverse('medical_query:add_query')