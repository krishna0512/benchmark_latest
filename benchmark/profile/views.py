from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView

from benchmark.models import Submission, Task, Dataset

class UserSubmissionListView(ListView):
    """Generic listbased view for user submissions.
    """
    
    model = Submission
    template_name = 'benchmark/profile/user_submission.html'
    content_object_name = 'submission_list'

    def get_queryset(self):
        """returns a queryset that contains only the submissions
        submitted by the current user.
        """
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UserSubmissionListView, self).get_context_data(**kwargs)
        # below code for fetching task_list is designed so that only
        # the tasks against which user has uploaded atleast one
        # submission is added to the task_list
        context['task_list'] = Task.objects.filter(
            datasets__in=Dataset.objects.filter(
                submissions__in=context['submission_list']
            ).distinct()
        ).distinct()
        return context

class UserUpdateProfile(UpdateView):
    """
    Final Template name = user_udpate_form.html
    """
    
    model = User
    fields = [
        'email',
        'first_name',
        'last_name'
    ]
    template_name = 'benchmark/profile/user_update.html'

    def get_success_url(self):
        """
        return to the same update users page after success of the update
        
        Note: Using request.path_info instead of request.path will make life
        easier when going from test to deployment servers
        """
        print('inside success_url')
        return self.request.path_info

    def form_valid(self, form):
        """If form is valid, Display the success message."""
        messages.success(self.request, 'User updated successfully.')
        return super().form_valid(form)

class PasswordChangeCustomView(PasswordChangeView):

    def get_success_url(self):
        messages.success(self.request, 'Your Password Changed successfully!')
        return reverse(
            'benchmark:user-submission',
            kwargs={
                'pk': self.request.user.id
            }
        )
