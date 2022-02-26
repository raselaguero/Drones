from django.contrib import admin
from .models import Drone, Medication

# Register your models here.


class MedicationInline(admin.TabularInline):
    model = Medication

@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model', 'weight_limit', 'battery_capacity', 'state')
    inlines = [MedicationInline]