from django.urls import path

from . import views

urlpatterns = [
    path('<int:route_pk>', views.assign_driver_to_a_route, name='assign-driver'),
    path('designate/route/', views.designate_route, name='designate-route'),
    path('backup/', views.backup_db, name='backup'),
    path('restore/', views.restore_db, name='restore')
]