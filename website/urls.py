"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from benchmark.resource import ApiSubmissionResource, DatasetImageResource

submission_resource = ApiSubmissionResource()
dataset_image_resource = DatasetImageResource()

urlpatterns = [
    # path('', include('benchmark.urls')),
    path('benchmark/', include('benchmark.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(submission_resource.urls)),
    path('api/', include(dataset_image_resource.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
