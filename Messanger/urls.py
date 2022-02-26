from django.urls import path
from Messanger import views
from Messanger import views as simple_views

urlpatterns = [
    path('emails/', views.SubscribeToHistoryList.as_view()),
    path('emails/<int:pk>/', views.SubscribeToHistoryDetails.as_view()),
    path('drones/', views.DroneList.as_view(), name='drone_list'),
    path('drones/<int:pk>/', views.DroneDetails.as_view(), name='drone_details'),
    path('drones/<int:pk>/battery-level/', simple_views.battery_capacity),
    path('drones/available-loading/', simple_views.drones_available_loading),
    path('medications/', views.MedicationList.as_view(), name='medication_list'),
    path('medications/<int:pk>/', views.MedicationDetails.as_view(), name='medication_details'),

]