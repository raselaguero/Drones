from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

MODEL_CHOICES = [
    ('Lightweight','Lightweight'),
    ('Middleweight','Middleweight'),
    ('Cruiserweight','Cruiserweight'),
    ('Heavyweight','Heavyweight'),
]

STATE_CHOICES = [
    ('IDLE', 'IDLE'),
    ('LOADING', 'LOADING'),
    ('LOADED', 'LOADED'),
    ('DELIVERING', 'DELIVERING'),
    ('DELIVERED', 'DELIVERED'),
    ('RETURNING', 'RETURNING'),
]

NAME_REGEX = RegexValidator(r'^[\w\-]+$', 'format invalid')
CODE_REGEX = RegexValidator(r'^[A-Z0-9\_]+$', 'format invalid')


class Drone(models.Model):
    serial_number = models.CharField(max_length=100, default='D355-M984', unique=True)
    model = models.CharField(max_length=13, choices=MODEL_CHOICES, default='Lightweight')
    weight_limit = models.FloatField('Weight Limit(gr)')
    battery_capacity = models.PositiveIntegerField('Battery Capacity(%)')
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='IDLE')

    def __str__(self):
        return self.serial_number

    class Meta:
       ordering = ['serial_number']


class Medication(models.Model):
    name = models.CharField(max_length=30, default='Aspirine', validators=[NAME_REGEX])
    weight = models.FloatField()
    code = models.CharField(max_length=15, default='MED_56912', unique=True, validators=[CODE_REGEX])
    image = models.ImageField(upload_to='static/images', blank=True)
    drone = models.ForeignKey('Drone', related_name='medications', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
       ordering = ['name']

