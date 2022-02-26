from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.http import HttpResponse
from datetime import datetime
from .models import Drone, Medication, SubscribeToHistory
from .serializers import DroneSerializer, MedicationSerializer, MedicationImageSerializer, SubscribeToHistorySerializer
from celery import shared_task
from Messanger.tasks import send_history_mail

# Create your views here.

class SubscribeToHistoryMixin(object):  #TODO: OK
    queryset = SubscribeToHistory.objects.all()
    serializer_class = SubscribeToHistorySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('email',)
    ordering_fields = ('email',)
    ordering = ['email']


class SubscribeToHistoryList(SubscribeToHistoryMixin, ListCreateAPIView):  #TODO: OK
    pass


class SubscribeToHistoryDetails(SubscribeToHistoryMixin, RetrieveUpdateDestroyAPIView):  #TODO: OK
    pass


class DroneMixin(object):  #TODO: OK
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('serial_number', 'model')
    ordering_fields = ('serial_number', 'model')
    ordering = ['serial_number']


class DroneList(DroneMixin, ListCreateAPIView):  #TODO: OK
    def post(self, request, *args, **kwargs):
        serializer = DroneSerializer(data=request.data)
        if serializer.is_valid():
            if not (int(request.data['battery_capacity']) < 25 and request.data['state'] == 'LOADING'):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error':'If the battery level is less than 25%, the status of the drone can not be charging...'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DroneDetails(DroneMixin, RetrieveUpdateDestroyAPIView):  #TODO: OK
    def put(self, request, *args, **kwargs):
        drone_instance = Drone.objects.get(pk=self.kwargs['pk'])
        if not ((int(request.data['battery_capacity']) < 25 and request.data['state'] == 'LOADING')
                or (drone_instance.battery_capacity < 25 and request.data['state'] == 'LOADING')
                or (int(request.data['battery_capacity']) < 25 and drone_instance.state == 'LOADING')):
            serializer = DroneSerializer(drone_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'If the battery level is less than 25%, the status of the drone can not be charging...'})


class MedicationMixin(object):  #TODO: OK
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'code')
    ordering_fields = ('name', 'code')
    ordering = ['name']


class MedicationList(MedicationMixin, ListCreateAPIView):  #TODO: OK
    def post(self, request, *args, **kwargs):
        med = Medication.objects.filter(drone=request.data['drone'])
        total_weight = sum([m.weight for m in med])
        if (total_weight + float(request.data['weight'])) < 500:
            serializer = MedicationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Exceeds the weight the drone can carry'})


class MedicationDetails(MedicationMixin, RetrieveUpdateDestroyAPIView):  #TODO: OK
    def put(self, request, *args, **kwargs):
        med_instance = Medication.objects.get(pk=self.kwargs['pk'])
        med = Medication.objects.filter(drone=request.data['drone']).exclude(pk=self.kwargs['pk'])
        total_weight = sum([m.weight for m in med])
        if (total_weight + float(request.data['weight'])) < 500:
            serializer = MedicationSerializer(med_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Exceeds the weight the drone can carry'})

    @parser_classes([MultiPartParser])  #TODO: OK
    def patch(self, request, *args, **kwargs):
        med_instance = Medication.objects.get(pk=self.kwargs['pk'])
        serializer = MedicationImageSerializer(med_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])  #TODO: OK
def battery_capacity(request, pk):
    if request.method == 'GET':
        try:
            dron = Drone.objects.get(pk=pk)
        except Drone.DoesNotExist:
            return HttpResponse(status=404)
        level = '{}%'.format(dron.battery_capacity)
        dic = {dron.serial_number: level}
        return Response(dic)


@api_view(['GET'])  #TODO: OK
def drones_available_loading(request):
    if request.method == 'GET':
        try:
            drones = Drone.objects.filter(battery_capacity__gte=25, state='IDLE')
        except Drone.DoesNotExist:
            return HttpResponse(status=404)
        levels = [(d.serial_number,{'battery_level':'{}%'.format(d.battery_capacity), 'state': d.state}) for d in drones]
        return Response(dict(levels))