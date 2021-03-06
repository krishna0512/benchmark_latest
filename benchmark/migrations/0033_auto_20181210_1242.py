# Generated by Django 2.0.8 on 2018-12-10 12:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('benchmark', '0032_auto_20181210_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.TextField(default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='language',
            name='description',
            field=models.TextField(default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='modality',
            name='description',
            field=models.TextField(default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='modality',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modality', to='benchmark.Document'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='year',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2100)]),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='task',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='benchmark.Document'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='taskcategory',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_category', to='benchmark.Language'),
        ),
        migrations.AlterField(
            model_name='taskcategory',
            name='modality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_category', to='benchmark.Modality'),
        ),
        migrations.AlterField(
            model_name='taskcategory',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_category', to='benchmark.Task'),
        ),
    ]
