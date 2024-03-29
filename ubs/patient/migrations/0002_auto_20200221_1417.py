# Generated by Django 2.2.6 on 2020-02-21 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='created_on',
            field=models.DateField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='city',
            name='updated_on',
            field=models.DateField(auto_now=True, verbose_name='Autalizado em'),
        ),
        migrations.AlterField(
            model_name='color',
            name='created_on',
            field=models.DateField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='color',
            name='updated_on',
            field=models.DateField(auto_now=True, verbose_name='Autalizado em'),
        ),
        migrations.AlterField(
            model_name='maritalstate',
            name='created_on',
            field=models.DateField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='maritalstate',
            name='updated_on',
            field=models.DateField(auto_now=True, verbose_name='Autalizado em'),
        ),
        migrations.AlterField(
            model_name='medicalinsurance',
            name='created_on',
            field=models.DateField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='medicalinsurance',
            name='updated_on',
            field=models.DateField(auto_now=True, verbose_name='Autalizado em'),
        ),
        migrations.AlterField(
            model_name='ocupation',
            name='created_on',
            field=models.DateField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='ocupation',
            name='updated_on',
            field=models.DateField(auto_now=True, verbose_name='Autalizado em'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='created_on',
            field=models.DateField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='updated_on',
            field=models.DateField(auto_now=True, verbose_name='Autalizado em'),
        ),
        migrations.AlterField(
            model_name='state',
            name='created_on',
            field=models.DateField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='state',
            name='updated_on',
            field=models.DateField(auto_now=True, verbose_name='Autalizado em'),
        ),
        migrations.AlterField(
            model_name='typelogradouro',
            name='created_on',
            field=models.DateField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='typelogradouro',
            name='updated_on',
            field=models.DateField(auto_now=True, verbose_name='Autalizado em'),
        ),
    ]
