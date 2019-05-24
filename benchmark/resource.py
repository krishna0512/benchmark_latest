# benchmark/resource.py

from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from benchmark.models import *

class ApiSubmissionResource(ModelResource):
    class Meta:
        queryset = ApiSubmission.objects.all()
        resource_name = 'submission'
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
