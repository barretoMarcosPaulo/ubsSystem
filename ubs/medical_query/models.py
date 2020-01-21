from django.db import models
from ubs.accounts.models import User
from ubs.core.models import AuditModel

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
        verbose_name = 'Consulta Medica'
        verbose_name_plural = 'Consultas Medicas'
        ordering = ['-created_on']

<<<<<<< HEAD


=======
>>>>>>> 1a9792efcc911cce7a2593bc78ae53543750e906
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

    full_name = models.CharField('Nome Completo',blank=True)
    date_birth = models.DateField('Data de Nascimento', blank=True)
    sex = models.CharField('Sexo',choices=sex_option)
    color = models.CharField('Cor')
    marital_state = models.CharField('Estado Conjugal', blank=True,choices=marital_state_option)
    ocupation = models.CharField('Ocupação')
    local_birth = models.CharField('Local de Nascimento')
    health_insurance = models.CharField('Convênio')
    phone = models.CharField('Telefone', blank=True)
    fax = models.CharField('fax')
    email = models.EmailField('email')

    def __str__(self):
        return self.full_name
    
    def get_absolute_url(self):
        return reverse("patient:register_patient")

    def Meta:
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
    physiological_personal_ antecedents = models.CharField('Altura', max_length=50, blank=False, null=False)

    def __int__(self):
        return self.patient

    def get_absolute_url(self):
        return reverse('medical_query:medical_querys_list')

    class Meta:
        verbose_name = 'Exame Fisico'
        verbose_name_plural = 'Exames Fisicos'
        ordering = ['-created_on']