import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Drones.settings')

app = Celery('Drones')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    'send-history-mail': {
        'task': 'Messanger.tasks.send_history_mail',
        'schedule': crontab(minute='*/5'),
    },
}