# Django specific imports
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView

# User specific imports
from benchmark import views

app_name = 'benchmark'
urlpatterns = [
    path(
        '',
        views.IndexListView.as_view(),
        name='home'
    ),

    path(
        'accounts/',
        include('django.contrib.auth.urls')
    ),

    path(
        'demo_alert/',
        TemplateView.as_view(template_name='benchmark/demo_alert.html'),
        name='demo_alert'
    ),

    path(
        'demo_stats/',
        TemplateView.as_view(template_name='benchmark/demo_stats.html'),
        name='demo_stats'
    ),

    path(
        'demo_proposal/',
        TemplateView.as_view(template_name='benchmark/demo_proposal.html'),
        name='demo_proposal'
    ),

    path(
        'demo_change_password/',
        TemplateView.as_view(template_name='benchmark/demo_change_password.html'),
        name='demo_change_password'
    ),

    path(
        'index/',
        views.IndexListView.as_view(),
        name='index'
    ),

    path(
        'about/',
        views.AboutTemplateView.as_view(),
        name='about'
    ),

    path(
        'resource/',
        views.ResourceListView.as_view(),
        name='resource'
    ),

    path(
        'challenge/',
        views.ChallengeTemplateView.as_view(),
        name='challenge'
    ),

    path(
        'register/',
        views.RegisterView.as_view(),
        name='register'
    ),

    # All the urls and views related to the user profile page
    # are stored in a seperate folder by name of profile
    path(
        'user/',
        include('benchmark.profile.urls'),
    ),

    path(
        'tasks/',
        views.TaskListView.as_view(),
        name='task-list'
    ),

    # online is for checking weather the user is viewing online
    # or offline submissions in task
    # 0  --  for offline submission
    # 1  --  for online submission
    path(
        'task/<int:pk>/<int:dataset_id>/<int:online>/',
        views.TaskDetailView.as_view(),
        name='task-detail'
    ),

    path(
        'task/4/',
        TemplateView.as_view(template_name='benchmark/task.html'),
        name='task'
    ),

    path(
        'submission/<int:pk>/delete/',
        views.SubmissionDeleteView.as_view(),
        name='delete-submission'
    ),

    path('confirm/', views.confirm_api_submission, name='confirm'),

    # path('leaderboard/upload_submission/<int:tc_id>', views.uploadSubmission, name='uploadSubmission'),
    path('task_controller/<int:task_id>', views.task_controller, name='task_controller'),

    path('delete_submission', views.delete_submission, name='delete_submission'),

    path('ajax/leaderboard_data/<int:tc_id>', views.getLeaderboardTableData, name='getLeaderboardTableData'),
    path('ajax/my_methods_data/<int:tc_id>', views.getmyMethodsTableData, name='getmyMethodsTableData'),
]
