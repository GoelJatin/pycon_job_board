from django.db import models

# Create your models here.
class Submitter(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    redact_email = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    code = models.PositiveSmallIntegerField()


class Job(models.Model):
    submitter = models.ForeignKey(
        Submitter,
        on_delete=models.CASCADE
    )
    company = models.CharField(max_length=100, null=False)
    website = models.URLField(null=False)

    title = models.CharField(max_length=100, null=False)
    job_url = models.URLField(null=False)
