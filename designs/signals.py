import os

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Comments, OrderDesign
from django.conf import settings

from .tasks import send_comment_in_mail_task

Users = get_user_model()
SITE_URL = SECRET_KEY = 'https://' + os.getenv('ALLOWED_HOST')


@receiver(post_save, sender=Comments)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:  # Отправляем только для новых комментариев
        order_design = instance.design
        author = instance.author
        recipient = None

        # Определяем получателя (если автор не владелец бриффа - отправляем владельцу)

        # Полный URL к изображению
        image_url = instance.image.url if instance.image else None
        if image_url:
            image_url = SITE_URL + image_url
            print('image_url', image_url)

        if author != order_design.user and order_design.user:
            recipient = order_design.user
        else:
            recipient = Users.objects.get(id=11)  ## HARD CODD FOR DESIGNER

        # Если получатель определен и у него есть email
        if recipient and recipient.email:
            subject = f'Новый комментарий к брифу "{order_design.title}"'
            message = render_to_string('emails/new_comment.html', {
                'recipient': recipient,
                'author': author,
                'order_design': order_design,
                'comment': instance,
                'image_url': image_url,

                'comment_url': SITE_URL + reverse('designs:design_detail', args=[order_design.id]),
                # 'unsubscribe_url': SITE_URL + reverse('profile_settings')
            })
            # print('Посылаю на почту----', recipient.email, message, )
            print('order_design', order_design)

            send_comment_in_mail_task.delay(
                subject,
                message,
                recipient = [recipient.email]
            )

