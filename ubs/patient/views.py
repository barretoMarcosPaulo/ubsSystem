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
import django_excel as excel


class PatientCreate(CreateView):
	model = Patient
	template_name = 'patient/add.html'
	form_class = PatientForm
	second_form_class = PhoneForm

	def get_context_data(self, **kwargs):
		ctx = super(PatientCreate, self).get_context_data(**kwargs)
		ctx['second_form'] = PhoneForm
		return ctx

	def post(self, request, *args, **kwargs):
        
		self.object = None
		form = self.form_class(self.request.POST , self.request.FILES)
		phone_form = self.second_form_class(self.request.POST)

		if form.is_valid() and phone_form.is_valid():
			return self.form_valid(form,phone_form)
		else:
			return self.form_invalid(form,phone_form)

	def form_valid(self,form,phone_form):

		with transaction.atomic():
			patient = form.save()
			phone = phone_form.save(commit=False)
			phone.Patient_idPatient = patient
			phone.save()
		
		return HttpResponseRedirect(reverse('patient:list_patient'))

	def form_invalid(self, form, address_form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
				address_form=address_form,
			)		
		)


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
	second_form_class = PhoneForm

	def get_context_data(self, **kwargs):
		self.object = self.get_object()
		phone = Phone.objects.get(Patient_idPatient=self.object.id)
		ctx = super(PatientUpdate, self).get_context_data(**kwargs)
		ctx['second_form'] = self.second_form_class(instance=phone)
		return ctx
	def post(self, request, *args, **kwargs):
        
		self.object = self.get_object()
		form = self.form_class(self.request.POST , self.request.FILES , instance=self.object)
		phone = Phone.objects.get(Patient_idPatient=self.object.id)
		phone_form = self.second_form_class(self.request.POST,instance=phone)

		if form.is_valid() and phone_form.is_valid():
			return self.form_valid(form,phone_form)
		else:
			return self.form_invalid(form,phone_form)

	def form_valid(self,form,phone_form):

		with transaction.atomic():
			patient = form.save()
			phone = phone_form.save(commit=False)
			phone.Patient_idPatient = patient
			phone.save()
		
		return HttpResponseRedirect(reverse('patient:list_patient'))

	def form_invalid(self, form, address_form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
				address_form=address_form,
			)		
		)

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
    form_class = PatientForm
    model = Patient
    second_form_class = PhoneForm

    def get_context_data(self, **kwargs):
        context = super(PatientDetail, self).get_context_data(**kwargs)
        # context["form"] = PatientForm 
        context["second_form"] = PhoneForm 
        context["second_model"] = Phone
        return context

#Initial City

class CityCreate(CreateView):
	model = City
	template_name = 'city/add.html'
	form_class = CityForm
		
	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.form_class(self.request.POST , self.request.FILES)
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self,form):
		with transaction.atomic():
			patient = form.save()
		
		return HttpResponseRedirect(reverse('patient:list_city'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)


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
	form_class = CityForm

	def get_context_data(self, **kwargs):
		self.object = self.get_object()
		ctx = super(CityUpdate, self).get_context_data(**kwargs)
		return ctx
	def post(self, request, *args, **kwargs):
        
		self.object = self.get_object()
		form = self.form_class(self.request.POST , self.request.FILES , instance=self.object)

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self,form):

		with transaction.atomic():
			city = form.save()
		
		return HttpResponseRedirect(reverse('patient:list_city'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)
 

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

# class PatientDetail(DetailView):
class CityDetail(UpdateView):

    model = City
    template_name = 'city/detail.html'
    form_class = CityDetailForm

    def get_context_data(self, **kwargs):
        _super = super(CityDetail, self)
        context = _super.get_context_data(**kwargs)
        context.update({
            'no_edit': True,
            })
        return context

class StateCreate(CreateView):
	model = State
	template_name = 'state/add.html'
	form_class = StateForm
		
	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.form_class(self.request.POST , self.request.FILES)
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self,form):
		with transaction.atomic():
			patient = form.save()
		
		return HttpResponseRedirect(reverse('patient:list_city'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

	def get_success_url(self):
		return reverse('patient:list_city')

class ListState(ListView):

    model = State
    http_method_names = ['get']
    template_name = 'state/list.html'
    context_object_name = 'object_list'
    paginate_by = 20


    def get_queryset(self):
        self.queryset = super(ListState, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
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

# class CityUpdate(UpdateView):
# 	model = City
# 	template_name = 'city/add.html'
# 	form_class = CityForm

# 	def get_context_data(self, **kwargs):
# 		self.object = self.get_object()
# 		ctx = super(CityUpdate, self).get_context_data(**kwargs)
# 		return ctx
# 	def post(self, request, *args, **kwargs):
        
# 		self.object = self.get_object()
# 		form = self.form_class(self.request.POST , self.request.FILES , instance=self.object)

# 		if form.is_valid():
# 			return self.form_valid(form)
# 		else:
# 			return self.form_invalid(form)

# 	def form_valid(self,form):

# 		with transaction.atomic():
# 			city = form.save()
		
# 		return HttpResponseRedirect(reverse('patient:list_city'))

# 	def form_invalid(self, form):
# 		return self.render_to_response(
# 			self.get_context_data(
# 				form=form,
# 			)		
# 		)
 

class DeleteState(DeleteView):
    model = State
    template_name="city/list.html"


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "Proposta excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa proposta não pôde ser excluída!", 'code': "0"})

# # class PatientDetail(DetailView):
# class CityDetail(UpdateView):

#     model = City
#     template_name = 'city/detail.html'
#     form_class = CityDetailForm

#     def get_context_data(self, **kwargs):
#         _super = super(CityDetail, self)
#         context = _super.get_context_data(**kwargs)
#         context.update({
#             'no_edit': True,
#             })
#         return context
