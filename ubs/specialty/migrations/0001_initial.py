# Generated by Django 2.2.6 on 2020-03-06 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalSpecialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('desc_specialty', models.CharField(max_length=100, verbose_name='Descrição especialidade(s)')),
            ],
            options={
                'verbose_name': 'Especialidade Médica',
                'verbose_name_plural': 'Especialidades Médicas',
            },
        ),
        migrations.CreateModel(
            name='DoctorHasMedicalSpecialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_on', models.DateField(auto_now=True, verbose_name='Autalizado em')),
                ('MedicalSpecialty_idSpecialty', models.ManyToManyField(to='specialty.MedicalSpecialty', verbose_name='Especialidade')),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Doctor', verbose_name='Médico')),
            ],
            options={
                'verbose_name': 'Especialidade',
                'verbose_name_plural': 'Especialidades',
            },
        ),
    ]
