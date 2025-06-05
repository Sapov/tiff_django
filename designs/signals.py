from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Comments


@receiver(post_save, sender=Comments)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:  # Только для новых комментариев
        design = instance.design
        project = design.project

        # Кому отправляем (клиенту или дизайнеру)
        recipient = project.client if instance.author == project.designer else project.designer
        subject = f'Новый комментарий к проекту "{project.title}"'
        message = render_to_string('emails/new_comment.html', {
            'recipient': recipient,
            'author': instance.author,
            'project': project,
            'comment': instance,
            'design_url': f'http://order.san-cd.ru/{reverse("project_detail", args=[project.id])}'
        })

        send_mail(
            subject,
            message,
            None,  # Используется DEFAULT_FROM_EMAIL
            [recipient.email],
            html_message=message,
            fail_silently=False
        )