from django.db import models
from ubs.core.models import AuditModel
from ubs.accounts.models import Doctor


class MedicalSpecialty(AuditModel):
    desc_specialty = models.CharField('Descrição especialidade(s)',max_length=100)

    class Meta:
        verbose_name = 'Especialidade Médica'
        verbose_name_plural = 'Especialidades Médicas'

class DoctorHasMedicalSpecialty(AuditModel):
    doctor = models.ManyToManyField(Doctor,verbose_name='Médico')
    MedicalSpecialty_idSpecialty = models.ForeignKey(MedicalSpecialty,verbose_name='Especialidade',null=True,blank=True,on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Especialidade'
        verbose_name_plural = 'Especialidades'
