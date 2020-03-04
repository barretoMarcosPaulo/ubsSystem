from django.shortcuts import render
# Create your views here.
from .forms import *
from .models import *

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse, reverse_lazy

from django.db import IntegrityError, transaction

from datetime import datetime
from ubs.patient.models import Patient

from django.db.models import Q
from .pusher import pusher_client

# Views for Querys
class QueryCreate(CreateView):
    model = Query
    template_name = 'querys/add.html'
    form_class = MedicalQueryForm
    second_form_class = PhisicalExamForm
    third_form_class = query_has_medicine_set_class


    def get(self, request,patient_pk,forwarding_pk,*args, **kwargs):
        pusher_client.trigger('my-channel', 'my-event', {'message': forwarding_pk})
        self.object = None
        patient = Patient.objects.get(id=patient_pk)
        
        # Set patient in atendance
        patient_forwarding = Forwarding.objects.get(patient=patient,id=forwarding_pk)
        patient_forwarding.in_attendance=True
        patient_forwarding.save()
        
        form = self.form_class
        second_form = self.second_form_class
        third_form_class = self.third_form_class()

        return self.render_to_response(
            self.get_context_data(
                form=form,
                second_form=second_form,
                patient=patient,
                third_form_class=third_form_class,
            )
        )

    def post(self, request, patient_pk, forwarding_pk, *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST, self.request.FILES)
        exam_form = self.second_form_class(self.request.POST)
        query_has_medicine_form = self.third_form_class(self.request.POST)

        patient_forwarding = Forwarding.objects.get(patient=patient_pk,id=forwarding_pk)
        patient_forwarding.in_attendance=False
        patient_forwarding.finalized=True
        patient_forwarding.save()


        if form.is_valid() and exam_form.is_valid() and exam_form.is_valid() and query_has_medicine_form.is_valid():
            return self.form_valid(form,exam_form,patient_pk,forwarding_pk,query_has_medicine_form )
        else:
            return self.form_invalid(form,exam_form, query_has_medicine_form)

    def form_valid(self, form, exam_form,patient_pk,forwarding_pk, query_has_medicine_form):
       
        with transaction.atomic():

            exam = exam_form.save()

            query = form.save(commit=False)
            query.medical = self.request.user
            query.PhisicalExam_idPhisicalExam = exam
            query.Patient_idPatient = Patient.objects.get(id=patient_pk)
            query.save()

            form.save_m2m()

            medicine = query_has_medicine_form.save(commit=False)
            for aux in medicine:
                aux.Query_idQuery = query         
                aux.save()


            pusher_client.trigger('my-channel-finalized', 'finalized', {'finalized': forwarding_pk})

            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, exam_form, query_has_medicine_form):
        return self.render_to_response(
            self.get_context_data(
                    form=form,
                    second_form=exam_form,
                    third_form_class=query_has_medicine_form,
                )
            )

    def get_success_url(self):
        return reverse('medical_query:list_query_history')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['third_form']=self.third_form_class
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
    form_class = MedicalQueryAttendanceForm
    second_form_class = PhisicalExamAttendanceForm


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
            self.queryset=self.queryset.filter(Q(main_complaint__icontains = self.request.GET['search_box']) | Q(current_health_history__icontains=self.request.GET['search_box']))
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
            self.queryset=self.queryset.filter(Q(main_complaint__icontains = self.request.GET['search_box']) | Q(current_health_history__icontains=self.request.GET['search_box']))
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

    def get_context_data(self, **kwargs):
        _super = super(Attendances, self)
        context = _super.get_context_data(**kwargs)
        physical_exam = PhisicalExam.objects.get(id=self.object.PhisicalExam_idPhisicalExam.id)
        context.update({
            'no_edit': True ,
            'second_form': self.second_form_class(instance=physical_exam),
            })
        return context


class ForwardingCreate(CreateView):
    model = Forwarding
    template_name = 'forwarding/add.html'
    form_class = ForwardingForm

    def get_success_url(self):
        return reverse('medical_query:await_querys_clerk')

class ForwardingList(ListView):
    model = Forwarding
    template_name = 'forwarding/list.html'
    http_method_names = ['get']
    paginate_by = 20

    

    def get_queryset(self):
        self.queryset = super(ForwardingList, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(patient__full_name__icontains = self.request.GET['search_box']) | Q(medical__full_name__icontains=self.request.GET['search_box']))
        return self.queryset

    def get_context_data(self, **kwargs):

        _super = super(ForwardingList, self)
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
            'currents_forwardings': Forwarding.objects.all(),
            'page_numbers': page_numbers,
            'show_first': 1 not in page_numbers,
            'show_last': num_pages not in page_numbers,
            })
        return context


class AwaitQuerys(ListView):
    model = Forwarding
    template_name = 'forwarding/await_querys.html'
    http_method_names = ['get']
    paginate_by = 20



    def get_queryset(self):
        self.queryset = super(AwaitQuerys, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(patient__full_name__icontains = self.request.GET['search_box']) | Q(medical__full_name__icontains=self.request.GET['search_box']))
        return self.queryset

    def get_context_data(self, **kwargs):

        _super = super(AwaitQuerys, self)
        context = _super.get_context_data(**kwargs)

        # not_priority =  Forwarding.objects.filter(created_on=datetime.now().date(), medical=self.request.user.id, priority=False).exclude(in_attendance=True)
        # priority =  Forwarding.objects.filter(created_on=datetime.now().date(), medical=self.request.user.id, priority=True).exclude(in_attendance=True)
        # list_values = []

        # p = list(priority)
        # n = list(not_priority)

        # count = 0
        # index_aux = 0 
        # count_p = 1 

        # if len(p) < len(n):
        #     for nao_prioritario in n:
        #         if count_p <= 2 and index_aux < len(p):
        #             n.insert(count,p[index_aux])
        #             index_aux+=1
        #             count_p+=1
        #         else:
        #             count_p=1
        #         count+=1
        #     list_values = n

        # else:

        #     for prioritario in p:
        #         if count_p == 3:
                    
        #             if index_aux == len(n):
        #                 break

        #             p.insert(count, n[index_aux])
        #             n.pop(index_aux)
        #             index_aux+=1
        #             count_p = 1
        #         else:
        #             count_p+=1
        #         count+=1

        #     for restante in n:
        #         p.append(restante)
        #     list_values= p
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
            'currents_forwardings': Forwarding.objects.filter(created_on=datetime.now().date(), medical=self.request.user.id),
            'page_numbers': page_numbers,
            'show_first': 1 not in page_numbers,
            'show_last': num_pages not in page_numbers,
            })
        return context



class AwaitQuerysClerk(ListView):
    model = Forwarding
    template_name = 'forwarding/await_querys_clerk.html'
    http_method_names = ['get']
    paginate_by = 20



    def get_queryset(self):
        self.queryset = super(AwaitQuerysClerk, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(patient__full_name__icontains = self.request.GET['search_box']) | Q(medical__full_name__icontains=self.request.GET['search_box']))
        return self.queryset

    def get_context_data(self, **kwargs):

        _super = super(AwaitQuerysClerk, self)
        context = _super.get_context_data(**kwargs)

        # not_priority =  Forwarding.objects.filter(created_on=datetime.now().date(), priority=False).exclude(in_attendance=True)
        # priority =  Forwarding.objects.filter(created_on=datetime.now().date(), priority=True).exclude(in_attendance=True)

        # not_priority =  Forwarding.objects.filter(created_on=datetime.now().date(), priority=False)
        # priority =  Forwarding.objects.filter(created_on=datetime.now().date(), priority=True)
       
        # list_values = []

        # p = list(priority)
        # n = list(not_priority)

        # count = 0
        # index_aux = 0 
        # count_p = 1 

        # if len(p) < len(n):
        #     for nao_prioritario in n:
        #         if count_p <= 2 and index_aux < len(p):
        #             n.insert(count,p[index_aux])
        #             index_aux+=1
        #             count_p+=1
        #         else:
        #             count_p=1
        #         count+=1
        #     list_values = n

        # else:

        #     for prioritario in p:
        #         if count_p == 3:
                    
        #             if index_aux == len(n):
        #                 break

        #             p.insert(count, n[index_aux])
        #             n.pop(index_aux)
        #             index_aux+=1
        #             count_p = 1
        #         else:
        #             count_p+=1
        #         count+=1

        #     for restante in n:
        #         p.append(restante)
        #     list_values= p

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
            'currents_forwardings': Forwarding.objects.filter(created_on=datetime.now().date()),
            'page_numbers': page_numbers,
            'show_first': 1 not in page_numbers,
            'show_last': num_pages not in page_numbers,
            })
        return context


class MedicineCreate(CreateView):
    model = Medicine
    template_name = 'medicine/add.html'
    form_class = MedicineForm

    def get_success_url(self):
        return reverse('medical_query:list_medicine')

class ListMedicine(ListView):

    model = Medicine
    template_name = 'medicine/list.html'
    context_object_name = 'object_list'
    http_method_names = ['get']
    paginate_by = 20

    
    def get_queryset(self):
        self.queryset = super(ListMedicine, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(generic_name__icontains = self.request.GET['search_box']))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListMedicine, self)
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

class MedicineUpdate(UpdateView):
    model = Medicine
    template_name = 'medicine/add.html'
    form_class = MedicineForm

    def get_success_url(self):
        return reverse('medical_query:list_medicine')

class MedicineDetail(UpdateView):
    model = Medicine
    template_name = 'medicine/detail.html'
    form_class = MedicineDetailForm
    
class DeleteMedicine(DeleteView):
    model = Medicine
    template_name="medicine/list.html"


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "Proposta excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa proposta não pôde ser excluída!", 'code': "0"})

class ExamRequestCreate(CreateView):
    model = ExamRequest
    template_name = 'exam_request/add.html'
    form_class = ExamRequestForm

    def get_success_url(self):
        return reverse('medical_query:list_exam_request')

class ListExamRequest(ListView):

    model = ExamRequest
    template_name = 'exam_request/list.html'
    context_object_name = 'object_list'
    http_method_names = ['get']
    paginate_by = 20

    
    def get_queryset(self):
        self.queryset = super(ListExamRequest, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(desc_exam__icontains = self.request.GET['search_box']))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListExamRequest, self)
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

class ExamRequestUpdate(UpdateView):
    model = ExamRequest
    template_name = 'exam_request/add.html'
    form_class = ExamRequestForm

    def get_success_url(self):
        return reverse('medical_query:list_exam_request')

class ExamRequestDetail(UpdateView):
    model = ExamRequest
    template_name = 'exam_request/detail.html'
    form_class = ExamRequestDetailForm
    
class DeleteExamRequest(DeleteView):
    model = ExamRequest
    template_name="exam_request/list.html"


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "Proposta excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa proposta não pôde ser excluída!", 'code': "0"})

class CID10Create(CreateView):
    model = CID10
    template_name = 'CID10/add.html'
    form_class = CID10Form

    def get_success_url(self):
        return reverse('medical_query:list_CID')

class ListCID10(ListView):

    model = CID10
    template_name = 'CID10/list.html'
    context_object_name = 'object_list'
    http_method_names = ['get']
    paginate_by = 20

    
    def get_queryset(self):
        self.queryset = super(ListCID10, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(desc_CID10__icontains = self.request.GET['search_box']))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ListCID10, self)
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

class CID10Update(UpdateView):
    model = CID10
    template_name = 'CID10/add.html'
    form_class = CID10EditForm

    def get_success_url(self):
        return reverse('medical_query:list_CID')

class CID10Detail(UpdateView):
    model = CID10
    template_name = 'CID10/detail.html'
    form_class = CID10DetailForm
    
class DeleteCID10(DeleteView):
    model = CID10
    template_name="CID10/list.html"


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return JsonResponse({'msg': "Proposta excluida com sucesso!", 'code': "1"})
        except:
            return JsonResponse({'msg': "Essa proposta não pôde ser excluída!", 'code': "0"})

class Recipe(DetailView):
    model = Query
    template_name="recipe/detail.html"
    form_class = MedicalQueryForm


