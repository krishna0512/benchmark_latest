import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, FormMixin, DeleteView

from benchmark.forms import UserRegistrationForm, SubmissionForm
from benchmark.models import Dataset, Resource, Submission, Task

# Create your views here.

class ResourceListView(ListView):
    """generic listbased views for resource
    default template name - 'benchmark/resource_list.html'
    default context object name - 'resource_list'
    """
    model = Resource
    context_object_name = 'resource_list'

class TaskListView(ListView):
    """Generic listbased view for selection of task
    context_object_name = 'task_list'
    template_name = 'benchmark/task_list.html'
    """
    model = Task

class TaskDetailView(FormMixin, DetailView):
    """Generic detailbased view for displaying individual task page.

    context_object_name = 'task'
    template_name = 'benchmark/task_detail.html'
    """
    model = Task
    form_class = SubmissionForm

    def get_success_url(self):
        return self.get_object().get_absolute_url()
        # return reverse(
            # 'benchmark:task-detail',
            # kwargs={
                # 'pk': self.object.id,
                # 'dataset_id': self.kwargs['dataset_id']
            # }
        # )

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context['form'] = SubmissionForm()
        context['online'] = self.kwargs['online']
        context['selected_dataset'] = Dataset.objects.get(
            id=self.kwargs['dataset_id']
        )
        submission_list = Submission.objects.filter(
            dataset__id=self.kwargs['dataset_id']
        ).filter(
            public=True
        )
        if self.kwargs['online']:
            context['submission_list'] = submission_list.filter(
                online=True
            )
        else:
            context['submission_list'] = submission_list.filter(
                online=False
            )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, 'Submission saved Successfully!')
        return super(TaskDetailView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Unable to save the submission')
        return super(TaskDetailView, self).form_invalid(form)

class RegisterView(View):
    context = {}
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'

    def render(self, request):
        return render(request, self.template_name, self.context)

    def add_new_user(self, form):
        """Inputs the form inputted to the POST method
        and outputs the newly created user which is not logged in.
        """
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        password = form.cleaned_data['password']
        user = User.objects.create_user(
            username,
            email,
            password,
            first_name=first_name,
            last_name=last_name
        )
        user.profile.affiliation_name = form.cleaned_data['affiliation_name']
        user.profile.dob = form.cleaned_data['dob']
        user.save()
        return authenticate(username=username, password=password)

    def get(self, request, *args, **kwargs):
        """Display empty form"""
        self.context['form'] = self.form_class()
        return self.render(request)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        self.context['form'] = form
        if form.is_valid():
            user = self.add_new_user(form)
            login(request, user)
            messages.success(request, 'User successfully registered and logged in')
            return redirect('benchmark:index')
        messages.error(request, 'Please check and correct the errors in form below.')
        return self.render(request)

def task_controller(request, task_id):
    name = Task.objects.get(id=task_id).name.lower()
    context = {}
    if 'block' in name:
        return render(request, 'benchmark/tasks_block.html', context)
    elif 'line' in name:
        return render(request, 'benchmark/tasks_line.html', context)
    elif 'word' in name:
        return render(request, 'benchmark/tasks_word.html', context)
    else:
        return render(request, 'benchmark/tasks_page.html', context)

# def uploadSubmission(request, tc_id):
    # """
    # This function will process the result of the submission form
    # and then will do all the preprocessing and redirect to the previous leaderboard page
    # the data for choosing the leaderboard page will come from the tc_id that is obtained via GET
    # """
    # tc = TaskCategory.objects.get(id=tc_id)
    # if request.method == 'POST':
        # form = SubmissionForm(request.POST, request.FILES, tc_id=tc_id)
        # if form.is_valid():
            # dataset = Dataset.objects.get(id=form.cleaned_data['dataset'])
            # user = request.user
            # title = form.cleaned_data['title']
            # description = form.cleaned_data['description']
            # authors = form.cleaned_data['authors']
            # paper_link = form.cleaned_data['paper_link']
            # is_result_public = form.cleaned_data['is_result_public']
            # s = Submission(
                # dataset=dataset,
                # user=user,
                # task_category=tc,
                # title=title,
                # description=description,
                # authors=authors,
                # paper_link=paper_link,
                # is_result_public=is_result_public,
                # result=request.FILES['result'],
                # # right now eval measure is random in the future we can use
                # # a job scheduler to schedule a job and compute the measures and
                # # only after that will the submission be saved in database.
                # # evaluation_measure_1 = str(get_evaluation_measure(request.FILES['result'])),
                # evaluation_measure_1='{0:.2f}'.format(random.uniform(20.0, 80.0)),
                # evaluation_measure_2='{0:.2f}'.format(random.uniform(20.0, 80.0)),
                # evaluation_measure_3='{0:.2f}'.format(random.uniform(20.0, 80.0)),
                # evaluation_measure_4='{0:.2f}'.format(random.uniform(20.0, 80.0))
            # )
            # s.save()
            # s.evaluate_measure()
            # # try:
                # # s.save()
                # # print('Saved submission form')
                # # if s.evaluate_measure():
                    # # messages.success(request, 'Submission form saved Successfully')
                # # else:
                    # # messages.error(request, 'Failed to Evaluate the Submission: No script for this task found')
            # # except:
                # # messages.error(request, 'Failed to save Submission form')
    # return redirect('benchmark:leaderboard', pk=tc_id)

def getLeaderboardTableData(request, tc_id):
    """Ajax view that returns the leaderboard table
    """
    data = []
    s = Submission.objects.filter(task_category__id=tc_id)
    for i in s:
        # functionlity for is_result_public
        if i.is_result_public or i.user == request.user:
            data.append(i.getJSONDict())
        else:
            pass
            # this submission should not be displayed to leaderboard
    return JsonResponse({'data':data})

def getmyMethodsTableData(request, tc_id):
    """Ajax view that returns mymethods table for logged in users
    """
    data = []
    s = Submission.objects.filter(task_category__id=tc_id).filter(user=request.user)
    for i in s:
        data.append(i.getJSONDict())
    return JsonResponse({'data':data})

class SubmissionDeleteView(UserPassesTestMixin, DeleteView):
    model = Submission

    def get(self, *args, **kwargs):
        """
        This function is required because to bypass the need
        for the confirm_delete page for django.
        When DeleteView is called  using GET by default it returns
        submission_confirm_delete.html page.
        This function overwrites that behaviour so that, it automatically
        acts as though it received YES signal in POST.
        """
        return self.post(*args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'You have deleted the submission successfully!')
        return self.request.GET.get('next','benchmark:index')

    def get_login_url(self):
        return reverse('benchmark:login')

    def test_func(self):
        if not self.request.user:
            messages.error(self.request, 'You cannot delete submission unless logged in!')
            return False
        messages.error(self.request, 'You don\'t have the permission to delete this Submission Instance')
        return self.get_object().user.id == self.request.user.id
