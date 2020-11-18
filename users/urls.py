from django.urls import path

from . import views

urlpatterns = [
    path('drivers/<int:pk>', views.DriverReadUpdateDeleteAPIView.as_view(), name='driver-detail'),
    path('drivers/', views.DriverListCreateAPIView.as_view(), name='driver-list'),
    path('car_types/', views.get_all_car_types, name='driver-car-types'),
    path('license_types/', views.get_all_license_types, name='driver-license-types'),
    path('register/manager', views.RegisterManager.as_view(), name="register-manager"),
    path('register/driver', views.RegisterDriver.as_view(), name="register-driver"),
    path('login/', views.CustomObtainAuthToken.as_view(), name="login"),
]
