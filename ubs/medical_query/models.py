from django.db import models
from ubs.accounts.models import User
from ubs.core.models import AuditModel


class Patient(AuditModel):
    sex_option = (
        ('Masculino','Masculino'),
        ('Feminino', 'Feminino'),
        ('Outro', 'Outro'),
    )

    marital_state_option = (
        ('Solteiro (a)', 'Solteiro (a)' ),
        ('Casado (a)', 'Casado (a)' ),
        ('Divorciado (a)', 'Divorciado (a)' ),
        ('Viúvo (a)', 'Viúvo (a)' ),
    ) 

    full_name = models.CharField('Nome Completo',blank=True,max_length=150)
    date_birth = models.DateField('Data de Nascimento')
    sex = models.CharField('Sexo',choices=sex_option,max_length=150)
    color = models.CharField('Cor',max_length=150)
    marital_state = models.CharField('Estado Conjugal',choices=marital_state_option,max_length=150)
    ocupation = models.CharField('Ocupação',max_length=150)
    local_birth = models.CharField('Local de Nascimento',max_length=150)
    health_insurance = models.CharField('Convênio',max_length=150)
    address = models.CharField('Endereço',max_length=150,null=True)
    phone = models.CharField('Telefone',max_length=150)
    fax = models.CharField('fax',max_length=150)
    email = models.EmailField('email',max_length=150)

    def __str__(self):
        return self.full_name
    
    def get_absolute_url(self):
        return reverse("patient:register_patient")

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-created_on']
    
class PhysicalExam(AuditModel):
    
    pa = models.CharField('PA', max_length=50)
    p = models.CharField('P', max_length=50)
    fc = models.TextField('FC', max_length=50, blank=False, null=False)
    epidemiological_history = models.CharField('FR', max_length=50, blank=False, null=False)
    previous_pathological_history = models.CharField('TAX', max_length=50, blank=False, null=False)
    family_history = models.CharField('Peso', max_length=50, blank=False, null=False)
    physiological_personal_antecedents = models.CharField('Altura', max_length=50, blank=False, null=False)

    def __int__(self):
        return self.pa

    def get_absolute_url(self):
        return reverse('medical_query:medical_querys_list')

    class Meta:
        verbose_name = 'Exame Fisico'
        verbose_name_plural = 'Exames Fisicos'
        ordering = ['-created_on']

class MedicalQuery(AuditModel):
    
    patient = models.ForeignKey(Patient , verbose_name="Paciente", null=True, blank=True, on_delete=models.SET_NULL)
    main_complaint = models.CharField('Queixa Principal', max_length=400, blank=False, null=False)
    current_health_history = models.CharField('Queixa Principal', max_length=400, blank=False, null=False)
    review_of_systems = models.TextField('Revisão de Sistemas', max_length=400, blank=False, null=False)
    epidemiological_history = models.CharField('História Epidemiológica', max_length=400, blank=False, null=False)
    previous_pathological_history = models.CharField('História Patológica Regressa', max_length=400, blank=False, null=False)
    family_history = models.CharField('História Familiar', max_length=400, blank=False, null=False)
    physiological_personal_antecedents = models.CharField('Antecedentes Pessoais Fisiológicas', max_length=400, blank=False, null=False)
    physical_exam = models.ForeignKey(PhysicalExam , verbose_name="Exame Físico", null=True, blank=True , on_delete=models.SET_NULL)
    summary = models.CharField('Sumário dos Postos Principais da História e Exame Físico', max_length=400, blank=False, null=False)
    Diagnostic_hypotheses = models.CharField('Hipótese(s) Diagnósticada(s)', max_length=400, blank=False, null=False)
    take_duct = models.CharField('Conduta Tomada', max_length=400, blank=False, null=False)
    medical = models.ForeignKey(User , verbose_name="Paciente", null=True, blank=True, on_delete=models.SET_NULL)

    def __int__(self):
        return self.patient

    def get_absolute_url(self):
        return reverse('medical_query:medical_querys_list')

    class Meta:
        verbose_name = 'Consulta Medica'
        verbose_name_plural = 'Consultas Medicas'
        ordering = ['-created_on']