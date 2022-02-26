from django.urls import path
from Messanger import views
from Messanger import views as simple_views

urlpatterns = [
    path('drones/', views.DroneList.as_view(), name='drone_list'),
    path('drones/<int:pk>/', views.DroneDetails.as_view(), name='drone_details'),
    path('drones/<int:pk>/battery-level/', simple_views.battery_capacity),
    #  path('drones/battery-level/', simple_views.drones_battery_capacity),
    path('drones/available-loading/', simple_views.drones_available_loading),
    path('medications/', views.MedicationList.as_view(), name='medication_list'),
    path('medications/<int:pk>/', views.MedicationDetails.as_view(), name='medication_details'),

    path('send-mail/', simple_views.send_mail)
]