from django import template
from django.template.defaultfilters import stringfilter

from ..models import Submitter

register = template.Library()


@register.filter
@stringfilter
def url_target_blank(url):
    return url.replace(
        '<a',
        '<a target="_blank"'
    )


@register.filter
@stringfilter
def redact_email(email):
    submitter = Submitter.objects.get(email=email)

    if submitter.redact_email:
        mail = email.split('@')[0]
        index = len(mail) // 2 // 2
        return email.replace(mail[index: -index], 'x' * (len(mail) - 2 * index))

    return email
