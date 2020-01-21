from django.db import models
from ubs.accounts.models import User

class MedicalQuery(AuditModel):
    
    patient = models.ForeignKey(Patient , verbose_name="Paciente", null=True, blank=True)
    main_complaint = models.CharField('Queixa Principal', max_length=400, blank=False, null=False)
    current_health_history = models.CharField('Queixa Principal', max_length=400, blank=False, null=False)
    review_of_systems = models.TextField('Revisão de Sistemas', max_length=400, blank=False, null=False)
    epidemiological_history = models.CharField('História Epidemiológica', max_length=400, blank=False, null=False)
    previous_pathological_history = models.CharField('História Patológica Regressa', max_length=400, blank=False, null=False)
    family_history = models.CharField('História Familiar', max_length=400, blank=False, null=False)
    physiological_personal_ antecedents = models.CharField('Antecedentes Pessoais Fisiológicas', max_length=400, blank=False, null=False)
    physical_exam = models.ForeignKey(PhysicalExam , verbose_name="Exame Físico", null=True, blank=True , on_delete=models.CASCADE)
    summary = models.CharField('Sumário dos Postos Principais da História e Exame Físico', max_length=400, blank=False, null=False)
    Diagnostic_hypotheses = models.CharField('Hipótese(s) Diagnósticada(s)', max_length=400, blank=False, null=False)
    take_duct = models.CharField('Conduta Tomada', max_length=400, blank=False, null=False)
    medical = models.ForeignKey(User , verbose_name="Paciente", null=True, blank=True)

    def __int__(self):
        return self.patient

    def get_absolute_url(self):
        return reverse('medical_query:medical_querys_list')

    class Meta:
        verbose_name = 'Publicar Competência'
        verbose_name_plural = 'Publicar Competências'
        ordering = ['-created_on']
