from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Comments, OrderDesign
from django.conf import settings

Users = get_user_model()


@receiver(post_save, sender=Comments)
def send_comment_notification(sender, instance, created, **kwargs):
    print('Написал КТО', instance.author)
    if created:  # Отправляем только для новых комментариев
        order_design = instance.design
        author = instance.author
        recipient = None

        # Определяем получателя (если автор не владелец бриффа - отправляем владельцу)
        print("ВладелEц", order_design.user, type(order_design.user))
        if author != order_design.user and order_design.user:
            recipient = order_design.user
        else:
            recipient = Users.objects.get(id=3) ## HARD CODD

        # Если получатель определен и у него есть email
        if recipient and recipient.email:
            subject = f'Новый комментарий к брифу "{order_design.title}"'
            message = render_to_string('emails/new_comment.html', {
                'recipient': recipient,
                'author': author,
                'order_design': order_design,
                'comment': instance,
                'comment_url': 'https://order.san-cd.ru' + reverse('designs:design_detail', args=[order_design.id]),
                # 'unsubscribe_url': 'https://order.san-cd.ru' + reverse('profile_settings')
            })
            print('Посылаю на почту----', recipient.email, message, )

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient.email],
                html_message=message,
                fail_silently=True
            )
