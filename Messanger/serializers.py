from rest_framework import serializers
from .models import Drone, Medication, SubscribeToHistory


class MedicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medication
        fields = ['id', 'name', 'weight', 'code', 'image', 'drone']
        read_only_fields = ('id', 'image')
        extra_kwargs = {'drone': {'required': False}}


class MedicationImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medication
        fields = ['image']


class DroneSerializer(serializers.ModelSerializer):
    medications = MedicationSerializer(many=True, read_only=True)

    class Meta:
        model = Drone
        fields = ['id', 'serial_number', 'model', 'weight_limit', 'battery_capacity', 'state', 'medications']
        read_only_fields = ('id',)


class SubscribeToHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscribeToHistory
        fields = ['email']
