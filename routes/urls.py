from django.urls import path

from . import views


urlpatterns = [
    path('<int:pk>', views.RouteReadUpdateDeleteAPIView.as_view(), name='route-detail'),
    path('', views.RouteListCreateAPIView.as_view(), name='route-list'),
    path('designated/<int:pk>', views.DesignatedRouteReadUpdateDeleteAPIView.as_view(), name='designated-route-detail'),
    path('designated/', views.DesignatedRouteListCreateAPIView.as_view(), name='designated-route-list'),
]