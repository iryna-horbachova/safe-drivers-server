from .models import Route, DesignatedRoute
from rest_framework import serializers

from users.models import Driver
from users.serializers import DriverSerializer


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id',
                  'title',
                  'priority',
                  'load_type',
                  'load_quantity',
                  'start_location',
                  'end_location',
                  'distance',
                  'min_health',
                  'min_experience',
                  'is_in_progress',
                  'manager']


class DesignatedRouteSerializer(serializers.ModelSerializer):
    route = RouteSerializer()
    driver = DriverSerializer()

    class Meta:
        model = DesignatedRoute
        fields = ['id',
                  'route',
                  'driver',
                  'status',]


