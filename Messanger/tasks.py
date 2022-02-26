from __future__ import absolute_import
from  celery import shared_task
from Drones.celery import app
from celery.utils.log import get_task_logger
from Drones.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from Messanger.models import Drone, SubscribeToHistory
from django.http import HttpResponse
from datetime import datetime

logger = get_task_logger(__name__)

@app.task
def send_history_mail():
    right_now = datetime.now()
    subject = 'battery capacity of the drones - {}'.format(right_now)
    try:
        subscribers = SubscribeToHistory.objects.all()
    except Drone.DoesNotExist:
        return HttpResponse(status=404)
    try:
        drones = Drone.objects.all()
    except Drone.DoesNotExist:
        return HttpResponse(status=404)
    levels = [(d.serial_number, '{}%'.format(d.battery_capacity)) for d in drones]
    levels.append(('date-time',right_now))
    recipients = [s.email for s in subscribers]
    message = dict(levels)
    send_mail(subject, message, EMAIL_HOST_USER, recipients, fail_silently=False)
