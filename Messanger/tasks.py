from  celery import shared_task
from Drones.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from Messanger.models import Drone
from django.http import HttpResponse
from datetime import datetime

@shared_task
def send_history_mail(subject, to):
    recipients = to.split(' ')
    try:
        drones = Drone.objects.all()
    except Drone.DoesNotExist:
        return HttpResponse(status=404)
    levels = [(d.serial_number, '{}%'.format(d.battery_capacity)) for d in drones]
    levels.append(('date-time', datetime.now()))
    message = dict(levels)
    send_mail(subject, message, EMAIL_HOST_USER, recipients, fail_silently=False)