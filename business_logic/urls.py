from django.urls import path

from . import views

urlpatterns = [
    path('<int:route_pk>', views.assign_driver_to_a_route, name='assign-driver'),
]

