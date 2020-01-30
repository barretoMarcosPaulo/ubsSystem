from django.db import models
from ubs.core.models import AuditModel
from django.urls import reverse

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
    
