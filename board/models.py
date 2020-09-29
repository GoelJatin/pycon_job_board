from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(primary_key=True)
    code = models.PositiveIntegerField()


class Submitter(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    redact_email = models.BooleanField(default=False)


class Job(models.Model):
    submitted_by = models.ForeignKey(
        Submitter,
        on_delete=models.CASCADE
    )
    company = models.CharField(max_length=100, null=False)
    website = models.URLField(null=False)

    title = models.CharField(max_length=100, null=False)
    job_url = models.URLField(null=True)
    description = models.CharField(max_length=100, null=True)
