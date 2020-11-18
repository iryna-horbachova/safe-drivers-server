from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from . import models
from . import serializers


class HealthConditionReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.HealthCondition.objects.all()
    serializer_class = serializers.HealthConditionSerializer


class HealthConditionListCreateAPIView(ListCreateAPIView):
    queryset = models.HealthCondition.objects.all()
    serializer_class = serializers.HealthConditionSerializer
