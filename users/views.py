from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from users import serializers, models


class CustomObtainAuthToken(views.ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class Logout(APIView):
    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterManager(generics.CreateAPIView):
    serializer_class = serializers.ManagerRegistrationSerializer
    queryset = models.Manager.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        user = models.User.objects.get(email=data['email'])
        token, _ = Token.objects.get_or_create(user=user)
        data['id'] = user.id
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class RegisterDriver(generics.CreateAPIView):
    serializer_class = serializers.DriverRegistrationSerializer
    queryset = models.Manager.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        user = models.User.objects.get(email=data['email'])
        token, _ = Token.objects.get_or_create(user=user)
        data['id'] = user.id
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class DriverReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Driver.objects.all()
    serializer_class = serializers.DriverSerializer


class DriverListCreateAPIView(ListCreateAPIView):
    queryset = models.Driver.objects.all()
    serializer_class = serializers.DriverSerializer


@api_view(http_method_names=['GET'])
def get_all_car_types(request):
    car_types = [{'db_value': car_types[0], 'title': car_types[1]} for car_types in models.Driver.CAR_TYPE_CHOICES]
    return Response(car_types)


@api_view(http_method_names=['GET'])
def get_all_license_types(request):
    license_types = [{'db_value': license_types[0], 'title': license_types[1]} for license_types in models.Driver.LICENSE_CHOICES]
    return Response(license_types)



