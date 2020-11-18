from .models import Route, DesignatedRoute
from rest_framework import serializers

from users.models import Driver


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id',
                  'priority',
                  'load_type',
                  'load_quantity',
                  'start_location',
                  'end_location',
                  'distance']


class DesignatedRouteSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all())

    class Meta:
        model = DesignatedRoute
        fields = ['route',
                  'driver',
                  'status',
                  'current_location']
