# Generated by Django 2.2.6 on 2020-02-29 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_clerk',
        ),
    ]
