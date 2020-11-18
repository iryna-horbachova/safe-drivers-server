from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.HealthConditionReadUpdateDeleteAPIView.as_view(), name='health-condition-detail'),
    path('', views.HealthConditionListCreateAPIView.as_view(), name='health-condition-list'),
]