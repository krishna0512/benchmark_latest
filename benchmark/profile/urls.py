# Django specific imports
from django.urls import path

# User specific imports
from benchmark.profile import views

urlpatterns = [
    path(
        '<int:pk>/submission/',
        views.UserSubmissionListView.as_view(),
        name='user_submission'
    ),

    path(
        '<int:pk>/update/',
        views.UserUpdateProfile.as_view(),
        name='user_update'
    ),
]
