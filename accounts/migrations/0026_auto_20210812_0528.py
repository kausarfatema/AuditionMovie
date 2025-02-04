# Generated by Django 3.2.4 on 2021-08-12 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20210811_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=250)),
                ('tin_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=300)),
                ('owner_name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='RecruterApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=60)),
                ('lasT_name', models.CharField(max_length=70)),
                ('company_name', models.CharField(max_length=100, null=True)),
                ('company_address', models.CharField(max_length=100, null=True)),
                ('tin_number', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=90)),
            ],
        ),
        migrations.AddField(
            model_name='recruter',
            name='rec_application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.recruterapp'),
        ),
    ]
