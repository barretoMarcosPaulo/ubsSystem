from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError, transaction

from .models import *
from ubs.accounts.models import Doctor
from .forms import *
from django.db.models import Q


class SpecialtyCreate(CreateView):
    model = MedicalSpecialty
    template_name = 'specialty/add.html'
    form_class = SpecialtyForm

    def get_success_url(self):
        return reverse('specialty:list_specialty')

class SpecialtyList(ListView):

    model = MedicalSpecialty
    http_method_names = ['get']
    template_name = 'specialty/list.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        self.queryset = super(SpecialtyList, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(desc_specialty__icontains = self.request.GET['search_box']))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(SpecialtyList, self)
        context = _super.get_context_data(**kwargs)
        adjacent_pages = 3
        page_number = context['page_obj'].number
        num_pages = context['paginator'].num_pages
        startPage = max(page_number - adjacent_pages, 1)
        if startPage <= 5:
            startPage = 1
        endPage = page_number + adjacent_pages + 1
        if endPage >= num_pages - 1:
            endPage = num_pages + 1
        page_numbers = [n for n in range(startPage, endPage) \
            if n > 0 and n <= num_pages]
        context.update({
            'page_numbers': page_numbers,
            'show_first': 1 not in page_numbers,
            'show_last': num_pages not in page_numbers,
            })
        return context


class SpecialtyUpdate(UpdateView):
    model = MedicalSpecialty
    template_name = 'specialty/edit.html'
    form_class = SpecialtyForm

    def get_success_url(self):
        return reverse('specialty:list_specialty')


class  SpecialtyDelete(DeleteView):
    model = MedicalSpecialty

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "especialidade excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa especialidade não pôde ser excluída!", 'code': "0"})



class DoctorSpecialtyCreate(CreateView):
    model = DoctorHasMedicalSpecialty
    template_name = 'doctor_specialty/add.html'
    form_class = DoctorSpecialtyForm

    def get_success_url(self):
        return reverse('specialty:list_doctor_specialty')

class DoctorSpecialtyList(ListView):

    model = DoctorHasMedicalSpecialty
    http_method_names = ['get']
    template_name = 'doctor_specialty/list.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        self.queryset = super(DoctorSpecialtyList, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(doctor__full_name__icontains = self.request.GET['search_box']) | Q(MedicalSpecialty_idSpecialty__desc_specialty__icontains=self.request.GET['search_box']))
            
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(DoctorSpecialtyList, self)
        context = _super.get_context_data(**kwargs)
        adjacent_pages = 3
        page_number = context['page_obj'].number
        num_pages = context['paginator'].num_pages
        startPage = max(page_number - adjacent_pages, 1)
        if startPage <= 5:
            startPage = 1
        endPage = page_number + adjacent_pages + 1
        if endPage >= num_pages - 1:
            endPage = num_pages + 1
        page_numbers = [n for n in range(startPage, endPage) \
            if n > 0 and n <= num_pages]
        context.update({
            'page_numbers': page_numbers,
            'show_first': 1 not in page_numbers,
            'show_last': num_pages not in page_numbers,
            })
        return context


class DoctorSpecialtyUpdate(UpdateView):
    model = DoctorHasMedicalSpecialty
    template_name = 'doctor_specialty/edit.html'
    form_class = DoctorSpecialtyForm

    def get_success_url(self):
        return reverse('specialty:list_doctor_specialty')


class  DoctorSpecialtyDelete(DeleteView):
    model = DoctorHasMedicalSpecialty

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "especialidade excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa especialidade não pôde ser excluída!", 'code': "0"})


