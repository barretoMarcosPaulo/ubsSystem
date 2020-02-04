from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.db import IntegrityError, transaction

from .models import User, Clerk ,Doctor, MedicalSpecialty, DoctorHasMedicalSpecialty
from .forms import UserAdminForm, UserClerkForm, UserDoctorForm

# Views for admin
class AdminCreate(CreateView):
    model = User
    template_name = 'users/add.html'
    form_class = UserAdminForm

    def post(self, request,  *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST , self.request.FILES)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        with transaction.atomic():
            admin = form.save(commit=False)
            admin.is_superuser = True
            admin.save()
        return HttpResponseRedirect(reverse('accounts:add_admin'))

    def form_invalid(self,form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )		
        )



# Views for clerk
class ClerkCreate(CreateView):
    model = Clerk
    template_name = 'users/add_clerk.html'
    form_class = UserClerkForm

    def post(self, request,  *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST , self.request.FILES)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        with transaction.atomic():
            clerk = form.save(commit=False)
            clerk.is_clerk = True
            clerk.save()
        return HttpResponseRedirect(reverse('accounts:add_admin'))

    def form_invalid(self,form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )		
        )


# Views for doctor
class DoctorCreate(CreateView):
    model = Doctor
    template_name = 'users/add.html'
    form_class = UserDoctorForm