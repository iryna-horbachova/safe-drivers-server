from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from . import models
from . import serializers


class DriverReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Driver.objects.all()
    serializer_class = serializers.DriverSerializer


class DriverListCreateAPIView(ListCreateAPIView):
    queryset = models.Driver.objects.all()
    serializer_class = serializers.DriverSerializer

    #def list(self, request, *args, **kwargs):
     #   queryset = self.filter_queryset(self.get_queryset())
      #  serializer = serializers.DriverSerializer(queryset.filter(manager__user=self.request.user), many=True)
       # return Response(serializer.data)


@api_view(http_method_names=['GET'])
def get_all_car_types(request):
    car_types = [{'db_value': car_types[0], 'title': car_types[1]} for car_types in models.Driver.CAR_TYPE_CHOICES]
    return Response(car_types)


@api_view(http_method_names=['GET'])
def get_all_license_types(request):
    license_types = [{'db_value': license_types[0], 'title': license_types[1]} for license_types in models.Driver.LICENSE_CHOICES]
    return Response(license_types)



