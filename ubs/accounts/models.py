import re
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core import validators
from django.db import models
from django.urls import reverse
from ubs.core.models import AuditModel
from ubs.specialty.models import DoctorHasMedicalSpecialty


class User(AbstractBaseUser, PermissionsMixin, AuditModel):

    username = models.CharField(
        "Usuário",
        max_length=200,
        default=uuid.uuid4,
        unique=True,
        validators=[
            validators.RegexValidator(
                re.compile("^[\w.@+-]+$"),
                "Informe um nome de usuário válido. "
                "Este valor deve conter apenas letras, números "
                "e os caracteres: @/./+/-/_ .",
                "invalid",
            )
        ],
        help_text="Um nome curto que será usado para identificá-lo de forma única na plataforma",
    )
    full_name = models.CharField("Nome Completo", max_length=100)
    cpf = models.CharField("CPF", max_length=14, unique="True")
    phone = models.CharField("Telefone", max_length=16)
    email = models.EmailField("Email", max_length=100, unique="True")
    is_staff = models.BooleanField("is staff", default=False)
    is_clerk = models.BooleanField("Atendente", default=False)
    is_doctor = models.BooleanField("Medico", default=False)

    def __str__(self):
        return self.full_name

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def get_absolute_url(self):
        return reverse("accounts:list_all_admin")

    def get_short_name(self):
        return self.full_name.split(" ")[0]

    def is_medical(self):
        try:
            Doctor.objects.get(id=self.id)
            return True
        except:
            return False

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


class Clerk(User):
    register_clerk = models.CharField("registro do técnico", max_length=12, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("accounts:list_all_clerk")


class Doctor(User):
    crm_doc = models.CharField("CRM do médico", max_length=20, blank=True, null=True)

    def get_specialts(self):
        list_specialts = []

        try:
            specialtys = DoctorHasMedicalSpecialty.objects.get(doctor=self)
            list_specialts = specialtys.MedicalSpecialty_idSpecialty.all()
        except:
            pass

        return list_specialts

    def get_absolute_url(self):
        return reverse("accounts:list_all_doctor")
