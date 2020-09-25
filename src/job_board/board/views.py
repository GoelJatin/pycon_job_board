from django.contrib import messages
from django.shortcuts import (
    render,
    redirect
)
from django.views import View

from .models import (
    Submitter,
    Job
)

from .forms import (
    SubmitterForm,
    JobForm
)

# Create your views here.
class JobView(View):

    def get(self, request):
        return render(
            request,
            'jobs.html',
            {
                'jobs': Job.objects.all()
            }
        )


class SubmitJobView(View):
    template = 'submit_job.html'

    def get(self, request):
        submitter_form = SubmitterForm()
        send_otp = True

        if 'email' in request.session:
            submitter = Submitter.objects.filter(email=request.session['email']).first()

            if submitter:
                submitter_form = SubmitterForm(instance=submitter)
                del submitter_form.fields['otp']
                send_otp = False

        return render(
            request,
            self.template,
            {
                'submitter_form': submitter_form,
                'job_form': JobForm(),
                'send_otp': send_otp
            }
        )

    def post(self, request):
        submitter_form = SubmitterForm(request.POST)
        job_form = JobForm(request.POST)

        if submitter_form.is_valid():
            if job_form.is_valid():
                submitter_form.save()

                job_form.cleaned_data['submitter'] = Submitter.objects.filter(email=submitter_form.cleaned_data['email']).first()
                job_form.save()

                request.session['email'] = submitter_form.cleaned_data['email']
                return redirect('/jobs')

        return render(
            request,
            self.template,
            {
                'submitter_form': submitter_form,
                'job_form': job_form
            }
        )
