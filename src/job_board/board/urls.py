from django.urls import path

from . import views


app_name = 'board'

urlpatterns = [
    path('', views.JobView.as_view(), name='jobs'),
    path('jobs', views.JobView.as_view(), name='jobs'),
    path('submit_job', views.SubmitJobView.as_view(), name='submit_job')
]
