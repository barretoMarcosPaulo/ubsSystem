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

from django.forms import formset_factory
from django.forms import modelformset_factory,inlineformset_factory


class PatientCreate(CreateView):
    model = Patient
    template_name = 'patient/add.html'
    form_class = PatientForm
    phone_formset_class = PhoneFormset


    def get(self, request, *args, **kwargs):
        self.phone_formset = self.phone_formset_class()
        self.phone_formset.extra=1    
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if not 'second_form' in kwargs:
            ctx['second_form'] = self.phone_formset
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST , self.request.FILES)
        phone_form = self.phone_formset_class(self.request.POST)

        if form.is_valid() and phone_form.is_valid():
            return self.form_valid(form,phone_form)
        else:
            return self.form_invalid(form,phone_form)

    def form_valid(self,form,phone_form):

        with transaction.atomic():
            patient = form.save()
            for phone_one_form in phone_form:
                phone = phone_one_form.save(commit=False)
                phone.Patient_idPatient = patient
                phone.save()
        
        return HttpResponseRedirect(reverse('patient:list_patient'))

    def form_invalid(self, form, address_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                second_form=address_form,
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
    phoneFormSet = PhoneFormset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        phone_objects = Phone.objects.filter(Patient_idPatient=self.object.id)
        self.second_form = self.phoneFormSet(instance=self.object, queryset=phone_objects)
        self.second_form.extra=0
        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        ctx = super(PatientUpdate, self).get_context_data(**kwargs)
        if not 'second_form' in kwargs:
            ctx['second_form'] = self.second_form
        return ctx

    def post(self, request, *args, **kwargs):
        # form = self.get_form()
        
        self.object = self.get_object()
        form = self.form_class(self.request.POST , self.request.FILES , instance=self.object)
        phone_form = self.phoneFormSet(self.request.POST,instance=self.object)

        if form.is_valid() and phone_form.is_valid():
            return self.form_valid(form,phone_form)
        else:
            return self.form_invalid(form,phone_form)

    def form_valid(self,form,phone_form):

        with transaction.atomic():
            patient = form.save()
            # phone = phone_form.save(commit=False)
            for phone_one_form in phone_form:
                phone = phone_one_form.save(commit=False)
                phone.Patient_idPatient = patient
                phone.save()
            # phone.Patient_idPatient = patient
            phone.save()
        
        return HttpResponseRedirect(reverse('patient:list_patient'))

    def form_invalid(self, form, address_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                second_form=address_form,
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
    form_class = PatientDetailForm
    model = Patient
    # second_form_class = PhoneForm

    # def get_context_data(self, **kwargs):
    #     context = super(PatientDetail, self).get_context_data(**kwargs)
    #     # context["form"] = PatientForm 
    #     context["second_form"] = PhoneForm 
    #     context["second_model"] = Phone
    #     return context
    
    def get_context_data(self, **kwargs):
        _super = super(PatientDetail, self)
        context = _super.get_context_data(**kwargs)
        context.update({
            'no_edit': True,
            })
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
	form_class = CityEditForm

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

#initial State
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
		
		return HttpResponseRedirect(reverse('patient:list_state'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

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

class StateUpdate(UpdateView):
	model = State
	template_name = 'state/add.html'
	form_class = StateEditForm

	def post(self, request, *args, **kwargs):
        
		self.object = self.get_object()
		form = self.form_class(self.request.POST , self.request.FILES , instance=self.object)

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self,form):

		with transaction.atomic():
		    state = form.save()
		
		return HttpResponseRedirect(reverse('patient:list_state'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

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

# class PatientDetail(DetailView):
class StateDetail(UpdateView):

    model = State
    template_name = 'state/detail.html'
    form_class = StateDetailForm

    def get_context_data(self, **kwargs):
        _super = super(StateDetail, self)
        context = _super.get_context_data(**kwargs)
        context.update({
            'no_edit': True,
            })
        return context

#initial MedicalInsurance
class MedicalInsuranceCreate(CreateView):
	model = MedicalInsurance
	template_name = 'medical_insurance/add.html'
	form_class = MedicalInsuranceForm
		
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
		
		return HttpResponseRedirect(reverse('patient:list_medical_insurance'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

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

	def post(self, request, *args, **kwargs):
        
		self.object = self.get_object()
		form = self.form_class(self.request.POST , self.request.FILES , instance=self.object)

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self,form):

		with transaction.atomic():
		    state = form.save()
		
		return HttpResponseRedirect(reverse('patient:list_medical_insurance'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

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

    def get_context_data(self, **kwargs):
        _super = super(MedicalInsuranceDetail, self)
        context = _super.get_context_data(**kwargs)
        context.update({
            'no_edit': True,
            })
        return context

class ColorCreate(CreateView):
	model = Color
	template_name = 'color/add.html'
	form_class = ColorForm
		
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
		
		return HttpResponseRedirect(reverse('patient:list_color'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

	def get_success_url(self):
		return reverse('patient:list_color')

#initial Color
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

	def post(self, request, *args, **kwargs):
        
		self.object = self.get_object()
		form = self.form_class(self.request.POST , self.request.FILES , instance=self.object)

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self,form):

		with transaction.atomic():
		    state = form.save()
		
		return HttpResponseRedirect(reverse('patient:list_color'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

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

    def get_context_data(self, **kwargs):
        _super = super(ColorDetail, self)
        context = _super.get_context_data(**kwargs)
        context.update({
            'no_edit': True,
            })
        return context

#initial MaritalState
class MaritalStateCreate(CreateView):
	model = MaritalState
	template_name = 'marital_state/add.html'
	form_class = MaritalStateForm
		
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
		
		return HttpResponseRedirect(reverse('patient:list_marital_state'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

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

	def post(self, request, *args, **kwargs):
        
		self.object = self.get_object()
		form = self.form_class(self.request.POST , self.request.FILES , instance=self.object)

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self,form):

		with transaction.atomic():
		    state = form.save()
		
		return HttpResponseRedirect(reverse('patient:list_marital_state'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

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

    def get_context_data(self, **kwargs):
        _super = super(MaritalStateDetail, self)
        context = _super.get_context_data(**kwargs)
        context.update({
            'no_edit': True,
            })
        return context

#initial TypeLogradouro
class TypeLogradouroCreate(CreateView):
	model = TypeLogradouro
	template_name = 'logradouro/add.html'
	form_class = TypeLogradouroForm
		
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
		
		return HttpResponseRedirect(reverse('patient:list_logradouro'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

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

class TypeLogradouroUpdate(UpdateView):
	model = TypeLogradouro
	template_name = 'logradouro/add.html'
	form_class = TypeLogradouroForm

	def post(self, request, *args, **kwargs):
        
		self.object = self.get_object()
		form = self.form_class(self.request.POST , self.request.FILES , instance=self.object)

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self,form):

		with transaction.atomic():
		    state = form.save()
		
		return HttpResponseRedirect(reverse('patient:list_logradouro'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

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

    def get_context_data(self, **kwargs):
        _super = super(TypeLogradouroDetail, self)
        context = _super.get_context_data(**kwargs)
        context.update({
            'no_edit': True,
            })
        return context

#initial TypeLogradouro
class OcupationCreate(CreateView):
	model = Ocupation
	template_name = 'ocupation/add.html'
	form_class = OcupationForm
		
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
		
		return HttpResponseRedirect(reverse('patient:list_ocupation'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

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

	def post(self, request, *args, **kwargs):
        
		self.object = self.get_object()
		form = self.form_class(self.request.POST , self.request.FILES , instance=self.object)

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self,form):

		with transaction.atomic():
		    state = form.save()
		
		return HttpResponseRedirect(reverse('patient:list_ocupation'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

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

    def get_context_data(self, **kwargs):
        _super = super(OcupationDetail, self)
        context = _super.get_context_data(**kwargs)
        context.update({
            'no_edit': True,
            })
        return context

#initial TypeLogradouro
class PhoneCreate(CreateView):
	model = Phone
	template_name = 'phone/add.html'
	form_class = PhoneFormAdmin
		
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
		
		return HttpResponseRedirect(reverse('patient:list_phone'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

	def get_success_url(self):
		return reverse('patient:list_phone')

class ListPhone(ListView):

    model = Phone
    http_method_names = ['get']
    template_name = 'phone/list.html'
    context_object_name = 'object_list'
    paginate_by = 20


    def get_queryset(self):
        self.queryset = super(ListPhone, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListPhone, self)
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

class PhoneUpdate(UpdateView):
	model = Phone
	template_name = 'phone/add.html'
	form_class = PhoneFormAdmin

	def post(self, request, *args, **kwargs):
        
		self.object = self.get_object()
		form = self.form_class(self.request.POST , self.request.FILES , instance=self.object)

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self,form):

		with transaction.atomic():
		    state = form.save()
		
		return HttpResponseRedirect(reverse('patient:list_phone'))

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)		
		)

class DeletePhone(DeleteView):
    model = Phone
    template_name="phone/list.html"


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "Proposta excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa proposta não pôde ser excluída!", 'code': "0"})

class PhoneDetail(UpdateView):

    model = Phone
    template_name = 'phone/detail.html'
    form_class = PhoneDetailForm

    def get_context_data(self, **kwargs):
        _super = super(PhoneDetail, self)
        context = _super.get_context_data(**kwargs)
        context.update({
            'no_edit': True,
            })
        return context
