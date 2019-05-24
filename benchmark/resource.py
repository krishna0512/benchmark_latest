# benchmark/resource.py

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from benchmark.models import *

class DatasetResource(ModelResource):
    class Meta:
        queryset = Dataset.objects.all()
        resource_name = 'dataset'
        fields = [
            'name',
            'description'
        ]
        allowed_methods = ['get']

class SubmissionResource(ModelResource):
    # Maps `Submission.dataset` to a Tastypie `ForeignKey` field named `dataset`,
    # which gets serialized using `DatasetResource`. The first appearance of
    # 'dataset' on the next line of code is the Tastypie field name, the 2nd
    # appearance tells the `ForeignKey` it maps to the `user` attribute of
    # `Submission`. Field names and model attributes don't have to be the same.
    dataset = fields.ForeignKey(DatasetResource, 'dataset')
    sample = fields.CharField(readonly=True)
    class Meta:
        queryset = Submission.objects.all()
        resource_name = 'submission'

    def dehydrate_sample(self, bundle):
        return bundle.obj.dataset.gtfile.url

class ApiSubmissionResource(ModelResource):
    class Meta:
        queryset = ApiSubmission.objects.all()
        # resource_name = 'submission'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle

class DatasetImageResource(ModelResource):
    class Meta:
        queryset = DatasetImage.objects.all()
        resource_name = 'dataset_image'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        fields = ['image']
