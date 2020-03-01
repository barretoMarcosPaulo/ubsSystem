from django.shortcuts import render
# Create your views here.
from .forms import *
from .models import *

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.db import IntegrityError, transaction
from django.http import HttpResponse, JsonResponse


class PatientCreate(CreateView):
    model = Patient
    template_name = 'patient/add.html'
    form_class = PatientForm
    success_url = 'patient/listagem-paciente'

    def get_success_url(self):
        return reverse('patient:list_patient')

class ListPatient(ListView):

    model = Patient
    http_method_names = ['get']
    template_name = 'patient/list.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        self.queryset = super(ListPatient, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListPatient, self)
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

class PatientUpdate(UpdateView):
    model = Patient
    template_name = 'patient/add.html'
    form_class = PatientForm

    def get_success_url(self):
        return reverse('patient:list_patient')

class DeletePatient(DeleteView):
    model = Patient
    template_name="patient/list.html"


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "Proposta excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa proposta não pôde ser excluída!", 'code': "0"})

class PatientDetail(UpdateView):
    template_name = 'patient/detail.html'
    form_class = PatientDetailForm
    model = Patient
        
#Initial City
class CityCreate(CreateView):
	model = City
	template_name = 'city/add.html'
	form_class = CityForm
		
	def get_success_url(self):
		return reverse('patient:list_city')

class ListCity(ListView):

    model = City
    http_method_names = ['get']
    template_name = 'city/list.html'
    context_object_name = 'object_list'
    paginate_by = 20


    def get_queryset(self):
        self.queryset = super(ListCity, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListCity, self)
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

class CityUpdate(UpdateView):
	model = City
	template_name = 'city/add.html'
	form_class = CityEditForm

	def get_success_url(self):
		return reverse('patient:list_city')

class DeleteCity(DeleteView):
    model = City
    template_name="city/list.html"


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "Proposta excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa proposta não pôde ser excluída!", 'code': "0"})

class CityDetail(UpdateView):

    model = City
    template_name = 'city/detail.html'
    form_class = CityDetailForm

#initial State
class StateCreate(CreateView):
	model = State
	template_name = 'state/add.html'
	form_class = StateForm

	def get_success_url(self):
		return reverse('patient:list_state')

class ListState(ListView):

    model = State
    http_method_names = ['get']
    template_name = 'state/list.html'
    context_object_name = 'object_list'
    paginate_by = 20


    def get_queryset(self):
        self.queryset = super(ListState, self).get_queryset()
        if self.request.GET.get('search_box', False) :
            self.queryset = self.queryset.filter(Q(title__contains = self.request.GET['search_box']) | Q(author__name__contains = self.request.GET['search_box']))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListState, self)
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

class StateUpdate(UpdateView):
	model = State
	template_name = 'state/add.html'
	form_class = StateEditForm

	def get_success_url(self):
		return reverse('patient:list_state')

class DeleteState(DeleteView):
    model = State
    template_name="state/list.html"


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "Proposta excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa proposta não pôde ser excluída!", 'code': "0"})

class StateDetail(UpdateView):

    model = State
    template_name = 'state/detail.html'
    form_class = StateDetailForm

#initial MedicalInsurance
class MedicalInsuranceCreate(CreateView):
	model = MedicalInsurance
	template_name = 'medical_insurance/add.html'
	form_class = MedicalInsuranceForm
		
	def get_success_url(self):
		return reverse('patient:list_medical_insurance')

class ListMedicalInsurance(ListView):

    model = MedicalInsurance
    http_method_names = ['get']
    template_name = 'medical_insurance/list.html'
    context_object_name = 'object_list'
    paginate_by = 20


    def get_queryset(self):
        self.queryset = super(ListMedicalInsurance, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListMedicalInsurance, self)
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

class MedicalInsuranceUpdate(UpdateView):
    model = MedicalInsurance
    template_name = 'medical_insurance/add.html'
    form_class = MedicalInsuranceForm
    
    def get_success_url(self):
        return reverse('patient:list_medical_insurance')

class DeleteMedicalInsurance(DeleteView):
    model = MedicalInsurance
    template_name="medica_insurance/list.html"


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "Proposta excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa proposta não pôde ser excluída!", 'code': "0"})

class MedicalInsuranceDetail(UpdateView):

    model = MedicalInsurance
    template_name = 'medical_insurance/detail.html'
    form_class = MedicalInsuranceDetailForm

#initial Color
class ColorCreate(CreateView):
	model = Color
	template_name = 'color/add.html'
	form_class = ColorForm
		
	def get_success_url(self):
		return reverse('patient:list_color')

class ListColor(ListView):

    model = Color
    http_method_names = ['get']
    template_name = 'color/list.html'
    context_object_name = 'object_list'
    paginate_by = 20


    def get_queryset(self):
        self.queryset = super(ListColor, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListColor, self)
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

class ColorUpdate(UpdateView):
	model = Color
	template_name = 'color/add.html'
	form_class = ColorForm

	def get_success_url(self):
		return reverse('patient:list_color')

class DeleteColor(DeleteView):
    model = Color
    template_name="cor/list.html"


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "Proposta excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa proposta não pôde ser excluída!", 'code': "0"})

class ColorDetail(UpdateView):

    model = Color
    template_name = 'color/detail.html'
    form_class = ColorDetailForm

#initial MaritalState
class MaritalStateCreate(CreateView):
	model = MaritalState
	template_name = 'marital_state/add.html'
	form_class = MaritalStateForm
		
	def get_success_url(self):
		return reverse('patient:list_marital_state')

class ListMaritalState(ListView):

    model = MaritalState
    http_method_names = ['get']
    template_name = 'marital_state/list.html'
    context_object_name = 'object_list'
    paginate_by = 20


    def get_queryset(self):
        self.queryset = super(ListMaritalState, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListMaritalState, self)
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

class MaritalStateUpdate(UpdateView):
	model = MaritalState
	template_name = 'marital_state/add.html'
	form_class = MaritalStateForm

	def get_success_url(self):
		return reverse('patient:list_marital_state')

class DeleteMaritalState(DeleteView):
    model = MaritalState
    template_name="marital_state/list.html"


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "Proposta excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa proposta não pôde ser excluída!", 'code': "0"})

class MaritalStateDetail(UpdateView):
    model = MaritalState
    template_name = 'marital_state/detail.html'
    form_class = MaritalStateDetailForm

#initial TypeLogradouro
class TypeLogradouroCreate(CreateView):
	model = TypeLogradouro
	template_name = 'logradouro/add.html'
	form_class = TypeLogradouroForm

	def get_success_url(self):
		return reverse('patient:list_logradouro')

class ListTypeLogradouro(ListView):

    model = TypeLogradouro
    http_method_names = ['get']
    template_name = 'logradouro/list.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        self.queryset = super(ListTypeLogradouro, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListTypeLogradouro, self)
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

    def get_success_url(self):
        return reverse('patient:list_logradouro')

class TypeLogradouroUpdate(UpdateView):
    model = TypeLogradouro
    template_name = 'logradouro/add.html'
    form_class = TypeLogradouroForm

    def get_success_url(self):
        return reverse('patient:list_logradouro')

class DeleteTypeLogradouro(DeleteView):
    model = TypeLogradouro
    template_name="logradouro/list.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "Proposta excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa proposta não pôde ser excluída!", 'code': "0"})

class TypeLogradouroDetail(UpdateView):

    model = TypeLogradouro
    template_name = 'logradouro/detail.html'
    form_class = TypeLogradouroDetailForm

#initial TypeLogradouro
class OcupationCreate(CreateView):
	model = Ocupation
	template_name = 'ocupation/add.html'
	form_class = OcupationForm
		
	def get_success_url(self):
		return reverse('patient:list_ocupation')

class ListOcupation(ListView):

    model = Ocupation
    http_method_names = ['get']
    template_name = 'ocupation/list.html'
    context_object_name = 'object_list'
    paginate_by = 20


    def get_queryset(self):
        self.queryset = super(ListOcupation, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListOcupation, self)
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

class OcupationUpdate(UpdateView):
	model = Ocupation
	template_name = 'ocupation/add.html'
	form_class = OcupationForm

	def get_success_url(self):
		return reverse('patient:list_ocupation')

class DeleteOcupation(DeleteView):
    model = Ocupation
    template_name="ocupation/list.html"


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "Proposta excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa proposta não pôde ser excluída!", 'code': "0"})

class OcupationDetail(UpdateView):

    model = Ocupation
    template_name = 'ocupation/detail.html'
    form_class = OcupationDetailForm
