from django.urls import path

from . import views

urlpatterns = [
    path('devices/', views.device_list),
    path('devices/<int:pk>/', views.device_detail, name='device-detail'),
]