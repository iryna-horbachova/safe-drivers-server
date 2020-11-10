from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.DriverReadUpdateDeleteAPIView.as_view(), name='driver-detail'),
    path('', views.DriverListCreateAPIView.as_view(), name='driver-list'),
    path('car_types/', views.get_all_car_types, name='driver-car-types'),
    path('license_types/', views.get_all_license_types, name='driver-license-types'),

#    path('login/', views.CustomObtainAuthToken.as_view(), name="login"),
 #   path('google-login/', views.ObtainGoogleAuthToken.as_view(), name="google-login"),
  #  path('<int:pk>/', views.UserDetail.as_view(), name="user-detail"),
   # path('logout/', views.Logout.as_view(), name="logout"),
    #path('register/', views.RegisterUser.as_view(), name="register")
]
