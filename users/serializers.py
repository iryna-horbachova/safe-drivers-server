from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Driver, Manager


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']

    def validate(self, attrs):
        password = attrs.get('password', None)
        confirm_password = attrs.get('confirm_password', None)

        if not password or password != confirm_password:
            raise ValidationError('password and confirm_password must be equal')

        return attrs


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = ['manager', 'car_type', 'experience', 'current_location', 'health_state', 'license_type']


class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Manager
        fields = ['company']
