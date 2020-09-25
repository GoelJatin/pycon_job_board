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
        cleaned_data = super(SubmitterForm, self).clean()

        if 'email' in cleaned_data:
            email = cleaned_data['email']

            if 'send_otp' in self.data:
                otp = random.randint(OTP_MIN_VALUE, OTP_MAX_VALUE)
                user = User.objects.filter(email=email).first()

                if user is None:
                    user = User.objects.create(email=email, code=otp)
                else:
                    user.code = otp

                user.save()
                raise ValidationError('Please provide the OTP sent to your email')
            else:
                user = User.objects.filter(email=email).first()

                if cleaned_data['otp'] != user.code:
                    raise ValidationError('OTP is invalid')

    def save(self):
        del self.cleaned_data['otp']
        submitter = Submitter.objects.create(**self.cleaned_data)
        submitter.save()


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        exclude = ('submitter',)

    def clean(self):
        cleaned_data = super(JobForm, self).clean()

        if 'website' in cleaned_data and 'job_url' in cleaned_data:
            # Run the validation calls concurrently to save time
            with ThreadPoolExecutor() as executor:
                is_valid_website = executor.submit(is_valid_url, cleaned_data['website'])
                is_valid_job_url = executor.submit(is_valid_url, cleaned_data['job_url'])

            if not is_valid_website.result():
                raise ValidationError('Website is not reachable, please provide a valid URL')

            if not is_valid_job_url.result():
                raise ValidationError('Job URL is not reachable, please check and validate')

    def save(self):
        job = Job.objects.create(**self.cleaned_data)
        job.save()
