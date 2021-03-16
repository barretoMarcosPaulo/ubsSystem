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

from dal import autocomplete

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



@method_decorator(login_required, name='dispatch')
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

        querys = Query.objects.filter(Patient_idPatient=patient_pk)
        
        last_query = None
        try:
            querys[0].created_on
        except:
            pass
        
        return self.render_to_response(
            self.get_context_data(
                form=form,
                second_form=second_form,
                patient=patient,
                third_form_class=third_form_class,
                patient_pk=patient_pk,
                forwarding_pk=forwarding_pk,
                last_query=last_query
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
            query.User_idUser = Doctor.objects.get(id=self.request.user.id)
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




@method_decorator(login_required, name='dispatch')
class QueryCancel(CreateView):
    model = Query
    template_name = 'querys/add.html'
    form_class = MedicalQueryForm



    def get(self, request,patient_pk,forwarding_pk,*args, **kwargs):
        pusher_client.trigger('cancel-query', 'cancel', {'message': self.request.user.id})
        self.object = None
        patient = Patient.objects.get(id=patient_pk)
        
        # # Set patient in atendance
        patient_forwarding = Forwarding.objects.get(patient=patient,id=forwarding_pk)
        patient_forwarding.in_attendance=False
        patient_forwarding.save()

        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        return reverse('medical_query:await_querys')

@method_decorator(login_required, name='dispatch')
class QueryUpdate(UpdateView):
    model = Query
    template_name = 'querys/add.html'
    form_class = MedicalQueryForm

    def get_success_url(self):
        return reverse('medical_query:list_query_history')




@method_decorator(login_required, name='dispatch')
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




@method_decorator(login_required, name='dispatch')
class ListQuerysHistory(ListView):

    model = Query
    http_method_names = ['get']
    template_name = 'querys/history.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        self.queryset = super(ListQuerysHistory, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(Patient_idPatient__full_name__icontains = self.request.GET['search_box']) | Q(current_health_history__icontains=self.request.GET['search_box']))
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
            'object_list': Query.objects.filter(User_idUser=self.request.user.id)
            })
        return context





@method_decorator(login_required, name='dispatch')
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




@method_decorator(login_required, name='dispatch')
class Attendances(UpdateView):

    model = Query
    template_name = 'querys/detail.html'
    form_class = MedicalQueryAttendanceForm
    second_form_class = PhisicalExamAttendanceForm

    def get_context_data(self, **kwargs):
        _super = super(Attendances, self)
        context = _super.get_context_data(**kwargs)
        medicines = QueryHasMedicine.objects.filter(Query_idQuery=self.object.id)
        physical_exam = PhisicalExam.objects.get(id=self.object.PhisicalExam_idPhisicalExam.id)
        context.update({
            'no_edit': True ,
            'second_form': self.second_form_class(instance=physical_exam),
            'medicines':medicines

            })
        return context




@method_decorator(login_required, name='dispatch')
class ForwardingCreate(CreateView):
    model = Forwarding
    template_name = 'forwarding/add.html'
    form_class = ForwardingForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST, self.request.FILES)

        if form.is_valid() :
            return self.form_valid(form)

    def form_valid(self, form):
        forwarding = form.save()
        pusher_client.trigger('notification', 'recieve-notification', {'message': forwarding.medical.id})

        return HttpResponseRedirect(self.get_success_url())



    def get_success_url(self):
        return reverse('medical_query:currents_forwarding')



@method_decorator(login_required, name='dispatch')
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




@method_decorator(login_required, name='dispatch')
class CurrentForwardingList(ListView):
    model = Forwarding
    template_name = 'forwarding/current_list.html'
    http_method_names = ['get']
    paginate_by = 20

    

    def get_queryset(self):
        self.queryset = super(CurrentForwardingList, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(patient__full_name__icontains = self.request.GET['search_box']) | Q(medical__full_name__icontains=self.request.GET['search_box']))
        return self.queryset

    def get_context_data(self, **kwargs):

        _super = super(CurrentForwardingList, self)
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
            'currents_forwardings': Forwarding.objects.filter(created_on=datetime.now().date()),
            'page_numbers': page_numbers,
            'show_first': 1 not in page_numbers,
            'show_last': num_pages not in page_numbers,
            })
        return context





@method_decorator(login_required, name='dispatch')
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





@method_decorator(login_required, name='dispatch')
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




@method_decorator(login_required, name='dispatch')
class MedicineCreate(CreateView):
    model = Medicine
    template_name = 'medicine/add.html'
    form_class = MedicineForm

    def get_success_url(self):
        return reverse('medical_query:list_medicine')



@method_decorator(login_required, name='dispatch')
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



@method_decorator(login_required, name='dispatch')
class MedicineUpdate(UpdateView):
    model = Medicine
    template_name = 'medicine/add.html'
    form_class = MedicineForm

    def get_success_url(self):
        return reverse('medical_query:list_medicine')



@method_decorator(login_required, name='dispatch')
class MedicineDetail(UpdateView):
    model = Medicine
    template_name = 'medicine/detail.html'
    form_class = MedicineDetailForm



@method_decorator(login_required, name='dispatch')
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



@method_decorator(login_required, name='dispatch')
class ExamRequestCreate(CreateView):
    model = ExamRequest
    template_name = 'exam_request/add.html'
    form_class = ExamRequestForm

    def get_success_url(self):
        return reverse('medical_query:list_exam_request')



@method_decorator(login_required, name='dispatch')
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



@method_decorator(login_required, name='dispatch')
class ExamRequestUpdate(UpdateView):
    model = ExamRequest
    template_name = 'exam_request/add.html'
    form_class = ExamRequestForm

    def get_success_url(self):
        return reverse('medical_query:list_exam_request')



@method_decorator(login_required, name='dispatch')
class ExamRequestDetail(UpdateView):
    model = ExamRequest
    template_name = 'exam_request/detail.html'
    form_class = ExamRequestDetailForm




@method_decorator(login_required, name='dispatch')
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



@method_decorator(login_required, name='dispatch')
class CID10Create(CreateView):
    model = CID10
    template_name = 'CID10/add.html'
    form_class = CID10Form

    def get_success_url(self):
        return reverse('medical_query:list_CID')



@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class CID10Update(UpdateView):
    model = CID10
    template_name = 'CID10/add.html'
    form_class = CID10EditForm

    def get_success_url(self):
        return reverse('medical_query:list_CID')


@method_decorator(login_required, name='dispatch')
class CID10Detail(UpdateView):
    model = CID10
    template_name = 'CID10/detail.html'
    form_class = CID10DetailForm

 
@method_decorator(login_required, name='dispatch')   
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


@method_decorator(login_required, name='dispatch')
class Recipe(DetailView):
    model = Query
    template_name="recipe/detail.html"
    form_class = MedicalQueryForm


    def get(self, request,query_pk,*args, **kwargs):
        self.object = None
        medicnes = QueryHasMedicine.objects.filter(Query_idQuery=query_pk)
        

        return self.render_to_response(
            self.get_context_data(
                current_date = datetime.now().date(),
                medicines = medicnes,
                object = Query.objects.get(id=query_pk)
            )
        )



@method_decorator(login_required, name='dispatch')
class ExamRequestPDF(DetailView):
    model = Query
    template_name="examRequest/examRequest.html"
    form_class = MedicalQueryForm


    def get(self, request,query_pk,*args, **kwargs):
        self.object = None

        return self.render_to_response(
            self.get_context_data(
                current_date = datetime.now().date(),
                object = Query.objects.get(id=query_pk)
            )
        )





@method_decorator(login_required, name='dispatch')
class ExamRequestAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        
        qs = ExamRequest.objects.all()

        if self.q:
            qs = qs.filter(Q(desc_exam__icontains=self.q))
        
        return qs


@method_decorator(login_required, name='dispatch')
class CID10Autocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        
        qs = CID10.objects.all()

        if self.q:
            qs = qs.filter(Q(desc_CID10__icontains=self.q))
        
        return qs



@method_decorator(login_required, name='dispatch')
class MedicineAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        
        qs = Medicine.objects.all()

        if self.q:
            qs = qs.filter(Q(generic_name__icontains=self.q))
        
        return qs