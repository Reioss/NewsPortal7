import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pro.settings')

app = Celery('pro')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'when_creating_new': {
        'task': 'task_add',
        'schedule': 30.0,
        'args': ("some_arg"),
    },
}

