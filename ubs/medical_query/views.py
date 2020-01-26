from django.shortcuts import render
# Create your views here.
from .forms import PatientForm,MedicalQueryForm
from .models import Patient,MedicalQuery

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.db import IntegrityError, transaction


class PatientCreate(CreateView):
    model = Patient
    template_name = 'patient/add.html'
    form_class = PatientForm

    def get_success_url(self):
        return reverse('medical_query:list_patient')

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

    # def form_valid(self, form):
    #     form.save()
    #     messages.success(self.request, 'Editado com sucesso.')
    #     return HttpResponseRedirect(self.get_success_url())

    # def form_invalid(self, form):
    #     messages.error(self.request, 'Ocorreu um erro ao atualizar os dados do paciente')
    #     return self.render_to_response(
    #         self.get_context_data(
    #         form=form
    #         )
    #     )

    def get_success_url(self):
        return reverse('medical_query:list_patient')


def delete_patient(request, id):
    patient = Patient.objects.get(id=id)
    patient.delete()
    return HttpResponseRedirect(reverse('medical_query:list_patient'))

class PatientDetail(DetailView):
	model = Patient
	template_name = 'patient/detail.html'
	form_class = PatientForm

class QueryCreate(CreateView):
    model = MedicalQuery
    template_name = 'querys/add.html'
    form_class = MedicalQueryForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class
        return self.render_to_response(
            self.get_context_data(
                form=form,
                
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST, self.request.FILES)
 
        if form.is_valid() :
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
       
        with transaction.atomic():

            query = form.save(commit=False)
            query.medical = self.request.user
            query.save()

            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print("Formulario Invalido")
        return self.render_to_response(
            self.get_context_data(
                    form=form,
                )
            )

    def get_success_url(self):
        return reverse('medical_query:add_query')


class ListQuerys(ListView):

    model = MedicalQuery
    http_method_names = ['get']
    template_name = 'querys/list.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        self.queryset = super(ListQuerys, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListQuerys, self)
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

class QueryUpdate(UpdateView):
    model = MedicalQuery
    template_name = 'querys/add.html'
    form_class = MedicalQueryForm




class QueryUpdate(UpdateView):
	model = MedicalQuery
	template_name = 'querys/add.html'
	form_class = MedicalQueryForm

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.form_class(instance=self.object)
		
		return self.render_to_response(
			self.get_context_data(
				form=form,	
			)
		)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.form_class(
			self.request.POST, self.request.FILES, instance=self.object)

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):

		with transaction.atomic():

			query = form.save(commit=False)
			query.medical = self.request.user
			query.save()


		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)
		)


class QueryDetail(DetailView):
	model = MedicalQuery
	template_name = 'querys/detail.html'
	form_class = MedicalQueryForm
