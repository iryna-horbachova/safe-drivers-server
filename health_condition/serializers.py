
from rest_framework import serializers

from health_condition.models import HealthCondition
from users.models import Driver
from users.serializers import DriverSerializer


class HealthConditionSerializer(serializers.ModelSerializer):
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all())
    #driver = DriverSerializer()
    class Meta:
        model = HealthCondition
        fields = [ 'id',
                    'driver',
                   'heart_rate',
                    'body_temperature',
                    'respiration_rate_per_minute',
                    'blood_pressure_systolic',
                    'blood_pressure_diastolic',
                    'blood_oxygen_level',
                    'blood_alcohol_content',
                    'drugs_alcohol_content',
                    'datetime' ]