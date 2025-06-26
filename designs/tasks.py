# tasks.py
import os

from celery import shared_task
from django.core.mail import send_mail

from mysite import settings
from .models import Comments


@shared_task
def send_comment_in_mail_task(
        subject,
        message,
        recipient,
        fail_silently=True
):
    # comment = Comments.objects.get(id=comment_id)
    send_mail(
            subject,
            message,
            os.getenv('EMAIL_HOST_USER'),
            recipient,
            html_message=message,
            fail_silently=True
        # )
    )

