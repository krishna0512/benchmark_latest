import datetime
import importlib
from zipfile import ZipFile

from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    affiliation_name = models.CharField(
        max_length=100,
        default='',
        verbose_name=_('Affiliation Name')
    )
    # If we pass the value of the function to default it results in the warning in django.
    # If we pass the value of func then default value will be set to date on which this module is imported.
    # instead of the date on which a new model is created.
    # To prevent that we pass the function datetime.date.today to the default
    dob = models.DateField(
        default=datetime.date.today,
        verbose_name=_('Date of Birth')
    )

    def get_profile_url(self):
        """
        returns the url for user submission page.
        """
        return reverse(
            'benchmark:user-submission',
            kwargs={
                'pk': self.user.id
            }
        )

class Announcement(models.Model):
    """
    This is model to hold all the announcement to be
    displayed in the home page
    """
    title = models.CharField(max_length=500)
    description = models.TextField(default='', blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return '{} ({})'.format(
            self.title,
            self.active
        )

class Alert(models.Model):
    """
    This is a model for storing user alerts.
    """
    title = models.CharField(max_length=300)
    message = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='alerts'
    )

    def __repr__(self):
        return '<Alert: {}>'.format(self.title)

    def __str__(self):
        return '{} ({})'.format(self.title, self.user.username)


class Resource(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(
        max_length=400,
        default='N/A',
        verbose_name=_('Author(s)')
    )
    year = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100)
        ],
        verbose_name=_('Year of Publication')
    )
    page_link = models.URLField(
        default='',
        verbose_name=_('Link to Paper')
    )
    pdf_link = models.URLField(
        default='',
        verbose_name=_('Link to Code')
    )

    def __repr__(self):
        if self.year:
            return '<Resource: {} ({})>'.format(self.title, self.year)
        else:
            return '<Resource: {}>'.format(self.title)

    def __str__(self):
        return self.title

class TaskImages(models.Model):
    image = models.ImageField(
        upload_to='task_images/'
    )

def task_directory_path(instance, filename):
    return 'Tasks/{}/{}'.format(instance.nickname, filename)

class Task(models.Model):
    name = models.CharField(max_length=200)
    nickname = models.CharField(
        max_length=30,
        default='',
        help_text=_('Field for storing the slug name for Task.')
    )
    display_image_1 = models.ImageField(
        upload_to=task_directory_path,
        null=True,
        verbose_name=_('First Display Image'),
        help_text=_('Field for storing the image displayed in task page.')
    )
    display_image_2 = models.ImageField(
        upload_to=task_directory_path,
        null=True,
        verbose_name=_('Second Display Image'),
        help_text=_('Field for storing the image displayed in task page.')
    )
    modality = models.CharField(
        max_length=100,
        default=''
    )
    language = models.CharField(
        max_length=100,
        default=''
    )
    purpose = models.CharField(
        max_length=100,
        default=''
    )
    description = models.TextField(default='')
    # Writeup for the Submission format modal in main task page.
    submission_format = models.TextField(default='')
    sample_submission = models.FileField(
        upload_to=task_directory_path,
        null=True,
        help_text=_('Sample ZIP-file format submission for this task')
    )
    sample_online_submission = models.FileField(
        upload_to=task_directory_path,
        null=True,
        help_text=_('Sample code file for online submission test')
    )
    em_description = models.TextField(
        default='No description Available',
        verbose_name=_('Evaluation Measure Description'),
        help_text=_('Writeup for describing the Evaluation Measures used in this task')
    )
    # Stores the path to a .py file that evaluates all the submissions
    # for this task.
    em_code = models.FileField(
        upload_to=task_directory_path,
        null=True,
        blank=True,
        verbose_name=_('Code for EM'),
        help_text=_('Code for Evaluation Measure (.py)')
    )

    def get_absolute_url(self):
        """
        returns the url for task-detail page for self
        """
        return reverse(
            'benchmark:task-detail',
            kwargs={
                'pk': self.id,
                'dataset_id': self.datasets.first().id,
                'online': 0
            }
        )

    def _get_evaluation_heading_from_em_code(self):
        """
        Returns a list of string that contains the
        heading for evaluation results for this task.
        this is obtained using the em_code path.
        """
        # Loading the evaluate function from the em_code file.
        spec = importlib.util.spec_from_file_location(
            'evaluate',
            self.em_code.path
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        try:
            ret = mod.evaluate()
        except:
            return None
        ret = [i for i in ret]
        return ret

    def get_evaluation_heading(self):
        """
        Returns a list of strings that contain the
        heading for evaluation results for this task.
        Note:
            If there are no submissions present in this task
            then the function returns a default Evaluation Heading (EM)
        """
        # Get all the submissions in this task
        s = Submission.objects.filter(
            dataset__task=self
        )
        ret = []
        if s.exists():
            ret = [i.name for i in s.first().evaluation_results.all()]
        else:
            ret = self._get_evaluation_heading_from_em_code() or ['EM']
        return ret

    def cleanup(self):
        """
        Function to clean and delete all the related uploaded
        files of the Task instance.
        False is so that after deleting the file model is NOT saved.
        """
        if self.display_image_1:
            self.display_image_1.delete(False)
        if self.display_image_2:
            self.display_image_2.delete(False)
        if self.sample_submission:
            self.sample_submission.delete(False)
        if self.sample_online_submission:
            self.sample_online_submission.delete(False)
        if self.em_code:
            self.em_code.delete(False)

    def __repr__(self):
        return '<Task: {} ({})>'.format(self.name, self.nickname)

    def __str__(self):
        return '{} ({})'.format(self.name, self.nickname)

    def __unicode__(self):
        return self.name

def dataset_directory_path(instance, filename):
    return 'Tasks/{}/Datasets/{}'.format(instance.task.nickname, filename)

class Dataset(models.Model):
    name = models.CharField(max_length=200)
    # Stores the complete description that goes in the link hover.
    description = models.TextField(default='')
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='datasets',
        help_text=_('Task that this dataset belongs to')
    )
    version = models.IntegerField(default=1)
    zipfile = models.FileField(
        upload_to=dataset_directory_path,
        null=True,
        verbose_name=_('Dataset File (.zip)'),
        help_text=_('Main dataset zip file containing images')
    )
    # number of images in zip file of dataset
    # mostly this is calculated automatically @ runtime
    nimages = models.PositiveIntegerField(
        default=0,
        blank=True,
        verbose_name=_('# of Images'),
        help_text=_('Number of Images in Dataset zip file is calculated automatically')
    )
    # This field is used for internal checking purpose regarding
    # weather the dataset uploaded is valid or not?
    # for e.g. the name of file in zipfile and filename in ground truth CSV should match
    valid = models.BooleanField(default=False)
    gtfile = models.FileField(
        upload_to=dataset_directory_path,
        null=True,
        verbose_name=_('Groudtruth File (.zip)'),
        help_text=_('Ground truth text files in zip')
    )

    def cleanup(self):
        """
        Function to clean and delete all the related uploaded
        files of the Dataset instance.
        False is so that after deleting the file model is NOT saved.
        """
        if self.zipfile:
            self.zipfile.delete(False)
        if self.gtfile:
            self.gtfile.delete(False)

    def get_absolute_url(self):
        """
        returns the url for task-detail page for self
        """
        return reverse(
            'benchmark:task-detail',
            kwargs={
                'pk': self.task.id,
                'dataset_id': self.id,
                'online': False
            }
        )

    def get_absolute_online_url(self):
        """
        returns the url for task-detail page for self
        """
        return reverse(
            'benchmark:task-detail',
            kwargs={
                'pk': self.task.id,
                'dataset_id': self.id,
                'online': True
            }
        )

    def get_download_link(self):
        return self.zipfile.url

    def __repr__(self):
        return '<Dataset-{}: {} ({})>'.format(self.version, self.name, self.task.name)

    def __str__(self):
        return '{} ({})'.format(self.name, self.version)

class DatasetImage(models.Model):
    image = models.FileField(
        upload_to='dataset/images/',
        null=True
    )
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='images'
    )

class ApiSubmission(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default='')
    authors = models.CharField(max_length=500)
    code_link = models.URLField(
        max_length=100,
        blank=True,
        default=''
    )
    paper_link = models.URLField(
        max_length=100,
        blank=True,
        default=''
    )
    result = models.TextField(default='')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='api_submission'
    )
    did = models.IntegerField(default=0)

def submission_directory_path(instance, filename):
    return 'Tasks/{}/Submissions/{}'.format(
        instance.dataset.task.nickname,
        filename
    )

class Submission(models.Model):
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='submissions',
        help_text=_('Dataset against which this submission is made.')
    )
    # TODO:
    # Verify what needs to be done if user that uploaded
    # the submission has his/her account deleted.
    # Current behaviour is that all the submissions by that user
    # will also be deleted and there is no archive remaining.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name=_('Method submitted by')
    )
    name = models.CharField(
        max_length=200,
        help_text=_('Short name of the method used')
    )
    description = models.TextField(
        default='',
        help_text=_('Brief description of the method employed')
    )
    # comma seperated list of authors
    authors = models.CharField(
        max_length=500,
        help_text=_('Comma seperated list of authors of this method')
    )
    code_link = models.URLField(
        max_length=100,
        blank=True,
        default='',
        verbose_name=_('Link to Code'),
        help_text=_('Please provide the full url for link')
    )
    paper_link = models.URLField(
        max_length=100,
        blank=True,
        default='',
        verbose_name=_('Link to Paper'),
        help_text=_(
            'URL to published paper referenced in this method.\
            <br>(Please provide the link to the page\
            instead of PDF link)'
            # 'URL to published paper referenced\
            # in this method (Please provide the link to\
            # the page instead of PDF)'
        )
    )
    result = models.FileField(
        upload_to=submission_directory_path,
        help_text=_('Uplaod a single ZIP file while adhering to the format specified'),
        null=True
    )
    public = models.BooleanField(
        default=True,
        verbose_name=_('Is result public?'),
        help_text=_('Check if the submission is to be displayed in public leaderboard')
    )
    online = models.BooleanField(
        default=False,
        verbose_name=_('Is this online submission?'),
        help_text=_('Check if the submission is listed under online submission')
    )
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Change the default ordering when accessing the Submission to
        # last_modified will come first
        ordering = ['-last_modified']

    def __repr__(self):
        return '<Submission: {}>'.format(self.name)

    def __str__(self):
        return self.name

    def cleanup(self):
        """
        Function to clean and delete all the related uploaded
        files of the Submission instance.
        False is so that after deleting the file model is NOT saved.
        """
        if self.result:
            self.result.delete(False)

    def get_evaluation_value(self):
        """
        returns a list of floats that contain the evaluation
        result for this submission.
        """
        return [i.value for i in self.evaluation_results.all()]

    def evaluate_submission(self):
        """
        Evaluates the Submission from the em_code in Task.
        assumes that the submission is already saved.
        this function is usually called from the post_save signal
        of the submission model.
        """
        if not self.dataset.task.em_code.path:
            print('No file for evaluating the submissions')
            return False
        # Loading the evaluate function from the em_code file.
        spec = importlib.util.spec_from_file_location(
            'evaluate',
            self.dataset.task.em_code.path
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if self.result:
            result = mod.evaluate(
                self.result.path,
                self.dataset.gtfile.path
            )
        else:
            result = mod.evaluate('','')
        # saving the result obtained from the em_code file to
        # the EvaluationResult Model.
        for key in result:
            EvaluationResult.objects.create(
                submission=self,
                name=key,
                value=round(float(result[key]),1)
            )


    def get_download_link(self):
        return self.result.url

class EvaluationResult(models.Model):
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='evaluation_results',
        help_text=_('To which submission does this evaluation result belong to?')
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('Evaluation Heading'),
        help_text=_('Key for the dict returned by the em_code')
    )
    value = models.FloatField(
        verbose_name=_('Evaluation Result'),
        help_text=_('Value for the dict returned by the em_code')
    )

    def __repr__(self):
        return '<EvaluationResult-{}: {} ({})>'.format(
            self.submission.id,
            self.name,
            self.value
        )

    def __str__(self):
        return '<EvaluationResult-{}: {} ({})>'.format(
            self.submission.id,
            self.name,
            self.value
        )

@receiver(post_save, sender=Submission)
def get_evaluation_results(sender, instance, created, **kwargs):
    """
    purpose of this function is to signal function is to call the
    evaluate submission func of the newly saved Submission instance
    """
    if created:
        instance.evaluate_submission()

@receiver(post_delete, sender=Submission)
def delete_submission_files(sender, instance, **kwargs):
    """
    Deleting the zip file from the filesystem after successfully deleting model instance
    """
    instance.cleanup()
    # if instance.result:
        # instance.result.delete(False)

@receiver(post_delete, sender=Task)
def delete_task_files(sender, instance, **kwargs):
    """
    Deleting all the stored files for a task when the task
    is deleted
    These files include the display images, and the code for EM.
    """
    instance.cleanup()


from benchmark.signals import *
