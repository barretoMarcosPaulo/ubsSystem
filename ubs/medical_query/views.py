from django.shortcuts import render
# Create your views here.
from .forms import MedicalQueryForm,MedicalQueryAttendanceForm
from .models import Query

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.db import IntegrityError, transaction


class QueryCreate(CreateView):
    model = Query
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


class ListQuerysHistory(ListView):

    model = Query
    http_method_names = ['get']
    template_name = 'querys/history.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        self.queryset = super(ListQuerysHistory, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListQuerysHistory, self)
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

class ListAttendances(ListView):

    model = Query
    http_method_names = ['get']
    template_name = 'querys/attendances.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        self.queryset = super(ListAttendances, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListAttendances, self)
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
    model = Query
    template_name = 'querys/add.html'
    form_class = MedicalQueryForm

    def get_success_url(self):
        return reverse('medical_query:list_query_history')



class QueryDetail(DetailView):
	model = Query
	template_name = 'querys/detail.html'
	form_class = MedicalQueryForm


class Attendances(UpdateView):

	model = Query
	template_name = 'querys/detail.html'
	form_class = MedicalQueryAttendanceForm
	
	# def get_object(self):
	# 	object_ = super().get_object()

	# 	if object_.em_atendimento:
	# 		setor = self.request.user.setor()	
	# 	else:
	# 		object_.em_atendimento=True
	# 		object_.save()
	# 		return object_

	# def form_valid(self,form_class):
	# 	object_ = super().get_object()
	# 	object_.em_atendimento=False
	# 	object_.save()
	# 	setor = self.request.user.setor()
		
	# 	ficha = FichaAtendimento.objects.filter(id=object_.id).first()
	# 	setor_user = Setor.objects.filter(id=setor).first()

	# 	AtendimentosRealizados.objects.create(ficha_usuario=ficha,setor_atendimento=setor_user)

	# 	return HttpResponseRedirect(reverse('atendimento:ficha_setor',kwargs={'pk':setor}))

	def get_context_data(self, **kwargs):
		_super = super(Attendances, self)
		context = _super.get_context_data(**kwargs)
		context.update({
			'no_edit': True ,
			})
		return context

	def get_success_url(self):
		return reverse('medical_query:list_attendances')