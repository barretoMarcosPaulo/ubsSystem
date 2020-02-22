from django.db import models

class AuditModel(models.Model):
	created_on = models.DateField('Criado em', auto_now_add=True)
	updated_on = models.DateField('Autalizado em', auto_now=True)

	class Meta:
		abstract=True