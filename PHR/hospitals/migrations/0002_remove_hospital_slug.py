# Generated by Django 2.0.1 on 2019-06-24 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospital',
            name='slug',
        ),
    ]
