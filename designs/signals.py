from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Comments, OrderDesign
from django.conf import settings


@receiver(post_save, sender=Comments)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:  # Отправляем только для новых комментариев
        order_design = instance.design
        author = instance.author
        recipient = None

        # Определяем получателя (если автор не владелец бриффа - отправляем владельцу)
        if author != order_design.user and order_design.user:
            recipient = order_design.user

        # Если получатель определен и у него есть email
        if recipient and recipient.email:
            subject = f'Новый комментарий к брифу "{order_design.title}"'
            message = render_to_string('emails/new_comment.html', {
                'recipient': recipient,
                'author': author,
                'order_design': order_design,
                'comment': instance,
                'comment_url': settings.SITE_URL + reverse('designs:design_detail', args=[order_design.id]),
                'unsubscribe_url': settings.SITE_URL + reverse('profile_settings')
            })

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient.email],
                html_message=message,
                fail_silently=True
            )