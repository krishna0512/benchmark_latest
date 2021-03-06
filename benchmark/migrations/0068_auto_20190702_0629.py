# Generated by Django 2.0.8 on 2019-07-02 06:29

import benchmark.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('benchmark', '0067_remove_submission_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='authors',
            field=models.CharField(help_text='Comma seperated list of authors of this method', max_length=500),
        ),
        migrations.AlterField(
            model_name='submission',
            name='code_link',
            field=models.URLField(blank=True, default='', help_text='Please provide the full url for link', max_length=100, verbose_name='Link to Code'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='description',
            field=models.TextField(default='', help_text='Brief description of the method employed'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='name',
            field=models.CharField(help_text='Short name of the method used', max_length=200),
        ),
        migrations.AlterField(
            model_name='submission',
            name='online',
            field=models.BooleanField(default=False, help_text='Check if the submission is listed under online submission', verbose_name='Is this online submission?'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='paper_link',
            field=models.URLField(blank=True, default='', help_text='URL to published paper referenced in this method.            <br>(Please provide the link to the page            instead of PDF link)', max_length=100, verbose_name='Link to Paper'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='public',
            field=models.BooleanField(default=True, help_text='Check if the submission is to be displayed in public leaderboard', verbose_name='Is result public?'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='result',
            field=models.FileField(help_text='Uplaod a single ZIP file while adhering to the format specified', null=True, upload_to=benchmark.models.submission_directory_path),
        ),
        migrations.AlterField(
            model_name='submission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=settings.AUTH_USER_MODEL, verbose_name='Method submitted by'),
        ),
    ]
