from django.shortcuts import render
from django.views.generic import TemplateView


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ubs.patient.models import Patient
from ubs.accounts.models import Doctor , Clerk
from ubs.medical_query.models import Query

@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = "core/base.html"

    def get_context_data(self, **kwargs):
        _super = super(IndexView, self)
        context = _super.get_context_data(**kwargs)
       

        if self.request.user.is_medical:
            context.update({
                'patients_count':Query.objects.filter(User_idUser=self.request.user.id).values('Patient_idPatient').distinct().count(),
                'doctors_count':Doctor.objects.count(),
                'clerks_count':Clerk.objects.count(),
                'querys_count':Query.objects.filter(User_idUser=self.request.user.id).count(),
                })
        else:
            context.update({
                'patients_count':Patient.objects.count(),
                'doctors_count':Doctor.objects.count(),
                'clerks_count':Clerk.objects.count(),
                'querys_count':Query.objects.count(),
                })   
                   
        return context