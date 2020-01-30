from django.shortcuts import render
# Create your views here.
from .forms import PatientForm
from .models import Patient

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
        return reverse('patient:list_patient')


def delete_patient(request, id):
    patient = Patient.objects.get(id=id)
    patient.delete()
    return HttpResponseRedirect(reverse('patient:list_patient'))  
 
class PatientDetail(DetailView):
	model = Patient
	template_name = 'patient/detail.html'
	form_class = PatientForm   

