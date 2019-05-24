from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BenchmarkConfig(AppConfig):
    """Main Appconfig 
    to install this app add the line
    'benchmark.apps.BenchmarkConfig' to your INSTALLED_APPS
    """
    name = 'benchmark'
    verbose_name = _('Indian Language Benchmark System')
