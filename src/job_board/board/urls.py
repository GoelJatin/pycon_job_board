from django.urls import path

from . import views


app_name = 'web'

urlpatterns = [
    # path('', views.JobView.as_view(), name='view_jobs'),
    # path('jobs', views.JobView.as_view(), name='view_jobs'),
    path('submit_job', views.SubmitJobView.as_view(), name='submit_job')
]
