# Generated by Django 2.2.6 on 2020-02-21 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='phone_number_main',
            field=models.CharField(max_length=13, unique=True, verbose_name='Número de telefone (principal)'),
        ),
        migrations.AlterField(
            model_name='state',
            name='region',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Região'),
        ),
    ]
