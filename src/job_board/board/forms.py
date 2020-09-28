from concurrent.futures import ThreadPoolExecutor

import random

from django import forms
from django.core.exceptions import ValidationError

from .models import (
    User,
    Submitter,
    Job
)
from .url_helper import is_valid_url

OTP_MIN_VALUE = 100000
OTP_MAX_VALUE = 999999


class SubmitterForm(forms.ModelForm):

    class Meta:
        model = Submitter
        fields = '__all__'

    otp = forms.IntegerField(min_value=OTP_MIN_VALUE, max_value=OTP_MAX_VALUE, required=False)

    def clean(self):
        email = self.data.get('email')
        self.cleaned_data['email'] = email

        try:
            # Don't raise any errors if cleanup is called for an existing submitter
            _ = Submitter.objects.get(email=email)
        except Submitter.DoesNotExist:
            cleaned_data = super(SubmitterForm, self).clean()

            # do futher validations only if email is valid
            if 'email' in cleaned_data:
                email = cleaned_data['email']

                if 'send_otp' in self.data:
                    otp = random.randint(OTP_MIN_VALUE, OTP_MAX_VALUE)
                    user, _ = User.objects.update_or_create(
                        defaults={'code': otp},
                        email=email
                    )
                    user.save()

                    # TODO: send otp to email
                    raise ValidationError('Please provide the OTP sent to your email')
                else:
                    user = User.objects.filter(email=email).first()

                    if user is None or cleaned_data['otp'] != user.code:
                        raise ValidationError('OTP is invalid')

    def save(self):
        del self.cleaned_data['otp']

        email = self.cleaned_data['email']
        del self.cleaned_data['email']

        submitter, _ = Submitter.objects.update_or_create(defaults=self.cleaned_data, email=email)
        submitter.save()

        User.objects.filter(email=email).delete()
        self.cleaned_data['email'] = email


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        exclude = ('submitted_by',)

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

        self.fields['job_url'].required = False
        self.fields['description'].required = False

    def clean(self):
        cleaned_data = super(JobForm, self).clean()

        if cleaned_data.get('job_url') is None and cleaned_data.get('description') is None:
            raise ValidationError('Either job url or description must be provided')

        is_valid_website = is_valid_job_url = None

        # Run the validation calls concurrently to save time
        with ThreadPoolExecutor() as executor:
            if 'website' in cleaned_data:
                is_valid_website = executor.submit(is_valid_url, cleaned_data['website'])

            if 'job_url' in cleaned_data and cleaned_data['job_url']:
                is_valid_job_url = executor.submit(is_valid_url, cleaned_data['job_url'])

        if is_valid_website and is_valid_website.result() is False:
            raise ValidationError('Website is not reachable, please provide a valid URL')

        if is_valid_job_url and is_valid_job_url.result() is False:
            raise ValidationError('Job URL is not reachable, please check and validate')

    def save(self):
        job = Job.objects.create(**self.cleaned_data)
        job.save()
