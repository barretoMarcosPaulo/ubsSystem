# Generated by Django 2.2.6 on 2020-02-28 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medical_query', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='Patient_idPatient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.Patient', verbose_name='Paciente'),
        ),
    ]
