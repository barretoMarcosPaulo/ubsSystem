# Generated by Django 2.2.6 on 2022-06-26 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20220626_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clerk',
            name='register_clerk',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='registro do técnico'),
        ),
    ]
