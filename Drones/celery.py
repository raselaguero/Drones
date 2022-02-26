import os
from celery import Celery
from Messanger.tasks import send_history_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Drones.settings')

app = Celery('Drones')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# @app.on_after_configure.connect
# #@app.on_after_finalize
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(60.0, send_my_email.s(''), name='Print name each 60 seconds')


@app.task
def send_my_email(subject, message, fromEmail, recipients):
    pass
    #send_mail(subject, message, fromEmail, recipients, fail_silently=False,)