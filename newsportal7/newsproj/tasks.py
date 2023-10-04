from celery import shared_task
from django.dispatch import receiver
from django.core.mail import mail_managers, send_mail
from .models import New


@shared_task
# создаём функцию обработчик с параметрами под регистрацию сигнала
@receiver(m2m_changed, sender=NewCategory)
def notify_news_create(sender, instance, **kwargs):
    if kwargs['action'] == 'news_create':
        categories = instance.category_new.all()
        subscribers: list[str] = []
        for category_new in categories:
            subscribers += category_new.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)
