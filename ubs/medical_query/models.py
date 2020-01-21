from django.db import models

# Create your models here.

class Patient(models.Model):
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
    


