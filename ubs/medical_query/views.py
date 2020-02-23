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

from datetime import datetime
from ubs.patient.models import Patient


# Views for Querys
class QueryCreate(CreateView):
    model = Query
    template_name = 'querys/add.html'
    form_class = MedicalQueryForm
    second_form_class = PhisicalExamForm
    third_form_class = QueryHasCID10Form


    def get(self, request,patient_pk,forwarding_pk,*args, **kwargs):
        self.object = None
        patient = Patient.objects.get(id=patient_pk)
        
        # Set patient in atendance
        patient_forwarding = Forwarding.objects.get(patient=patient,id=forwarding_pk)
        patient_forwarding.in_attendance=True
        patient_forwarding.save()
        
        form = self.form_class
        second_form = self.second_form_class
        third_form_class = self.third_form_class

        return self.render_to_response(
            self.get_context_data(
                form=form,
                second_form=second_form,
                third_form_class=third_form_class,
                patient=patient
                
            )
        )

    def post(self, request, patient_pk, forwarding_pk, *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST, self.request.FILES)
        exam_form = self.second_form_class(self.request.POST)
        cdi_form = self.third_form_class(self.request.POST)

        
        if form.is_valid() and exam_form.is_valid() :
            return self.form_valid(form,exam_form,cdi_form, patient_pk)
        else:
            return self.form_invalid(form,exam_form,cdi_form)

    def form_valid(self, form, exam_form, cdi_form, patient_pk):
       
        with transaction.atomic():

            exam = exam_form.save()
            cdi = cdi_form.save(commit=False)
 
            query = form.save(commit=False)
            query.medical = self.request.user
            query.PhisicalExam_idPhisicalExam = exam
            query.Patient_idPatient = Patient.objects.get(id=patient_pk)
            query.save()
            cdi.Query_idQuery_CID = query;

            cdi.save()

            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, exam_form, cdi_form):
        print("Formulario Invalido")
        return self.render_to_response(
            self.get_context_data(
                    form=form,
                )
            )

    def get_success_url(self):
        return reverse('medical_query:list_query_history')


class QueryUpdate(UpdateView):
    model = Query
    template_name = 'querys/add.html'
    form_class = MedicalQueryForm

    def get_success_url(self):
        return reverse('medical_query:list_query_history')


class QueryDetail(DetailView):
    model = Query
    template_name = 'querys/detail.html'
    form_class = MedicalQueryAttendanceForm
    second_form_class = PhisicalExamAttendanceForm
    third_form_class = QueryHasCID10Form

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class
        second_form = self.second_form_class
       

        return self.render_to_response(
            self.get_context_data(
                form=form,
                second_form=second_form
            )
        )

# Views for history attendances
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


class Attendances(UpdateView):

    model = Query
    template_name = 'querys/detail.html'
    form_class = MedicalQueryAttendanceForm
    second_form_class = PhisicalExamAttendanceForm
    third_form_class = QueryHasCID10Form

    def get_context_data(self, **kwargs):
        _super = super(Attendances, self)
        context = _super.get_context_data(**kwargs)
        physical_exam = PhisicalExam.objects.get(id=self.object.PhisicalExam_idPhisicalExam.id)
        cid = QueryHasCID10.objects.get(Query_idQuery_CID=self.object.id)
        context.update({
            'no_edit': True ,
            'second_form': self.second_form_class(instance=physical_exam),
            'cid10': cid
            })
        return context


class ForwardingCreate(CreateView):
    model = Forwarding
    template_name = 'forwarding/add.html'
    form_class = ForwardingForm

    def get_success_url(self):
        return reverse('medical_query:currents_forwarding')

class ForwardingList(ListView):
    model = Forwarding
    template_name = 'forwarding/list.html'
 
    

    def get_queryset(self):
        self.queryset = super(ForwardingList, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):

        _super = super(ForwardingList, self)
        context = _super.get_context_data(**kwargs)

       
        context.update({
            'currents_forwardings': Forwarding.objects.all()
            })
        return context


class AwaitQuerys(ListView):
    model = Forwarding
    template_name = 'forwarding/await_querys.html'


    def get_queryset(self):
        self.queryset = super(AwaitQuerys, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):

        _super = super(AwaitQuerys, self)
        context = _super.get_context_data(**kwargs)

       
        context.update({
            'currents_forwardings': Forwarding.objects.filter(created_on=datetime.now().date(), medical=self.request.user.id).exclude(in_attendance=True)
            })
        return context