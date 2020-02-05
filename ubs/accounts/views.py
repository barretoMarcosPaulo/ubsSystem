from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.db import IntegrityError, transaction

from .models import User, Clerk ,Doctor, MedicalSpecialty, DoctorHasMedicalSpecialty
from .forms import UserAdminForm, UserClerkForm, UserDoctorForm

# Views for admin

# Create
class AdminCreate(CreateView):
    model = User
    template_name = 'users/admin/add.html'
    form_class = UserAdminForm

    def post(self, request,  *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST , self.request.FILES)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        with transaction.atomic():
            admin = form.save(commit=False)
            admin.is_superuser = True
            admin.save()
        return HttpResponseRedirect(reverse('accounts:list_all_admin'))

    def form_invalid(self,form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )		
        )


#List
class AdminList(ListView):

    model = User
    http_method_names = ['get']
    template_name = 'users/admin/list.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        self.queryset = super(AdminList, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(AdminList, self)
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




# Views for clerk
class ClerkCreate(CreateView):
    model = Clerk
    template_name = 'users/clerk/add.html'
    form_class = UserClerkForm

    def post(self, request,  *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST , self.request.FILES)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        with transaction.atomic():
            clerk = form.save(commit=False)
            clerk.is_clerk = True
            clerk.save()
        return HttpResponseRedirect(reverse('accounts:aaccounts:list_all_clerk'))

    def form_invalid(self,form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )		
        )


class ClerkList(ListView):

    model = Clerk
    http_method_names = ['get']
    template_name = 'users/clerk/list.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        self.queryset = super(ClerkList, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(ClerkList, self)
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




# Views for doctor
class DoctorCreate(CreateView):
    model = Doctor
    template_name = 'users/doctor/add.html'
    form_class = UserDoctorForm

    def post(self, request,  *args, **kwargs):
        self.object = None
        form = self.form_class(self.request.POST , self.request.FILES)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        with transaction.atomic():
            doctor = form.save(commit=False)
            doctor.is_doctor = True
            doctor.save()
        return HttpResponseRedirect(reverse('accounts:list_all_doctor'))

    def form_invalid(self,form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )		
        )


class DoctorList(ListView):

    model = Doctor
    http_method_names = ['get']
    template_name = 'users/doctor/list.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        self.queryset = super(DoctorList, self).get_queryset()
        if self.request.GET.get('search_box', False):
            self.queryset=self.queryset.filter(Q(full_name__icontains = self.request.GET['search_box']) | Q(first_name__icontains=self.q))
        return self.queryset

    def get_context_data(self, **kwargs):
        _super = super(DoctorList, self)
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