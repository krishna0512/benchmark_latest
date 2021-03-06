# Generated by Django 2.0.8 on 2019-04-15 08:06

import benchmark.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benchmark', '0054_task_sample_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='em_code',
            field=models.FileField(blank=True, help_text='Code for Evaluation Measure (.py)', null=True, upload_to=benchmark.models.task_directory_path, verbose_name='Code for EM'),
        ),
        migrations.AddField(
            model_name='task',
            name='em_description',
            field=models.TextField(default='No description Available', help_text='Writeup for describing the Evaluation Measures used in this task', verbose_name='Evaluation Measure Description'),
        ),
        migrations.AlterField(
            model_name='task',
            name='sample_submission',
            field=models.FileField(help_text='Sample ZIP-file format submission for this task', null=True, upload_to=benchmark.models.task_directory_path),
        ),
    ]
