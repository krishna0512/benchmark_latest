# Generated by Django 2.0.8 on 2019-04-15 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benchmark', '0055_auto_20190415_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='em_result',
            field=models.CharField(default={}, max_length=500),
            preserve_default=False,
        ),
    ]
