from django.db import models
from ubs.core.models import AuditModel


class MedicalSpecialty(AuditModel):
    desc_specialty = models.CharField('Descrição especialidade(s)',max_length=100)

    def __str__(self):
        return self.desc_specialty

    class Meta:
        verbose_name = 'Especialidade Médica'
        verbose_name_plural = 'Especialidades Médicas'

class DoctorHasMedicalSpecialty(AuditModel):
    doctor = models.ForeignKey('accounts.Doctor',verbose_name='Médico',null=True,blank=True,on_delete=models.SET_NULL)
    MedicalSpecialty_idSpecialty = models.ManyToManyField(MedicalSpecialty,verbose_name='Especialidade')

    class Meta:
        verbose_name = 'Especialidade'
        verbose_name_plural = 'Especialidades'
