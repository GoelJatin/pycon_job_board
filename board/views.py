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
                'columns': [field.verbose_name.capitalize() for field in Job._meta.fields],
                'jobs': Job.objects.all()
            }
        )


class SubmitJobView(View):
    template = 'submit_job.html'

    def get(self, request):
        submitter_form = SubmitterForm()
        send_otp = True

        if 'email' in request.session:
            try:
                submitter = Submitter.objects.get(email=request.session['email'])
                submitter_form = SubmitterForm(instance=submitter)
                submitter_form.fields['email'].disabled = True

                del submitter_form.fields['otp']
                send_otp = False
            except Submitter.DoesNotExist:
                pass

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
        send_otp = True
        post_data = request.POST.copy()

        if 'email' in request.session:
            post_data['email'] = request.session['email']
            send_otp = False

        submitter_form = SubmitterForm(post_data)
        job_form = JobForm(post_data)

        if submitter_form.is_valid():
            if job_form.is_valid():
                submitter_form.save()

                job_form.cleaned_data['submitted_by'] = Submitter.objects.get(email=submitter_form.cleaned_data['email'])
                job_form.save()

                request.session['email'] = submitter_form.cleaned_data['email']
                return redirect('/jobs')

        if not send_otp:
            del submitter_form.fields['otp']

            # submitter_form.fields['email'].disabled = True
            submitter_form.fields['email'].required = False

        return render(
            request,
            self.template,
            {
                'submitter_form': submitter_form,
                'job_form': job_form,
                'send_otp': send_otp
            }
        )
