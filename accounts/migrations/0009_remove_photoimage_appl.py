# Generated by Django 3.2.4 on 2021-07-23 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_photoimage_appl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photoimage',
            name='appl',
        ),
    ]
