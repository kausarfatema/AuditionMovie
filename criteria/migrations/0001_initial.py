# Generated by Django 3.2.4 on 2021-07-19 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0006_auto_20210617_1727'),
        ('ads', '0002_application_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField()),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.ad')),
                ('talent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.talent')),
            ],
        ),
        migrations.CreateModel(
            name='CriteriaQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField()),
                ('question', models.CharField(max_length=600)),
                ('option1', models.CharField(max_length=200)),
                ('option2', models.CharField(max_length=200)),
                ('option3', models.CharField(max_length=200)),
                ('option4', models.CharField(max_length=200)),
                ('answer', models.CharField(choices=[('Option1', 'Option1'), ('Option2', 'Option2'), ('Option3', 'Option3'), ('Option4', 'Option4')], max_length=200)),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.ad')),
            ],
        ),
    ]
