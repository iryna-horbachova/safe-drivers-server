from .models import User, Driver, Manager
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'id']


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = ['user', 'manager', 'car_type', 'experience', 'current_location', 'health_state', 'license_type']


class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Manager
        fields = ['user', 'company']


class DriverRegistrationSerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,)
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)
    car_type = serializers.CharField(min_length=1, write_only=True)
    car_max_load = serializers.IntegerField(write_only=True)
    experience = serializers.IntegerField(write_only=True)
    pay_for_km = serializers.IntegerField(write_only=True)
    average_speed_per_hour = serializers.IntegerField(write_only=True)
    license_type = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password',
                  'car_type', 'car_max_load', 'experience', 'pay_for_km', 'average_speed_per_hour', 'license_type']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        password2 = attrs.get('confirm_password')

        user = User.objects.filter(email=email).first()

        if user:
            msg = _('Email must be unique.')
            raise serializers.ValidationError(msg)

        if password != password2:
            msg = _('"Password1" and "Password2" must be equal.')
            raise serializers.ValidationError(msg)
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']

        user = User.objects.create_user(email=email, username=email,
                                        password=password, is_manager=True,
                                        first_name=first_name, last_name=last_name)

        request = self.context.get('request', None)

        if request:
            requested_user = request.user

        manager_user = User.objects.filter(id=requested_user.id)[0]
        manager = Manager.objects.filter(user=manager_user)[0]

        car_type = validated_data['car_type']
        car_max_load = validated_data['car_max_load']
        experience = validated_data['experience']
        pay_for_km = validated_data['pay_for_km']
        average_speed_per_hour = validated_data['average_speed_per_hour']
        license_type = validated_data['license_type']

        driver = Driver.objects.create(user=user, manager=manager, car_type=car_type,
                                       car_max_load=car_max_load, experience=experience,
                                       pay_for_km=pay_for_km, average_speed_per_hour=average_speed_per_hour,
                                       license_type=license_type)
        return user


class ManagerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)
    company = serializers.CharField(min_length=3, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password', 'company']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        password2 = attrs.get('confirm_password')

        user = User.objects.filter(email=email).first()

        if user:
            msg = _('Email must be unique.')
            raise serializers.ValidationError(msg)

        if password != password2:
            msg = _('"Password1" and "Password2" must be equal.')
            raise serializers.ValidationError(msg)
        return attrs

    def create(self, validated_data):

        company = validated_data['company']
        validated_data.pop('confirm_password')
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        company = validated_data['company']
        user = User.objects.create_user(email=email, username=email,
                                        password=password, is_manager=True,
                                        first_name=first_name, last_name=last_name)

        manager = Manager.objects.create(user=user, company=company)

        return user


class UserChangeSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'image']
