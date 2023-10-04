from django.db.models.signals import m2m_changed
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html
from django.dispatch import receiver  # импортируем нужный декоратор
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from .models import New, Category, NewCategory, Author
from django.contrib.auth.models import Group, User

def send_notifications(preview, pk, title,subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email='schersvetlana@yandex.ru',
        to=subscribers,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()

@receiver(m2m_changed, sender=NewCategory)
def notify_news_create(sender, instance, **kwargs):
    if kwargs['action'] == 'news_create':
        categories = instance.category_new.all()
        subscribers: list[str] = []
        for category_new in categories:
            subscribers += category_new.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)