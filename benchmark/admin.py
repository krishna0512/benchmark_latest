from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from benchmark.models import *

class DatasetAdmin(admin.ModelAdmin):
    """
    Changes:
    Makes the field nimages readonly as that value can only
    be added programmitically.
    """
    readonly_fields = ('nimages',)

admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Resource)
admin.site.register(Submission)
admin.site.register(Task)
admin.site.register(EvaluationResult)
admin.site.register(ApiSubmission)
admin.site.register(DatasetImage)
admin.site.register(Announcement)

class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInLine,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
