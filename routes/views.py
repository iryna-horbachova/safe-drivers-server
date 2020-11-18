from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response

from . import models
from . import serializers


class RouteReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Route.objects.all()
    serializer_class = serializers.RouteSerializer


class RouteListCreateAPIView(ListCreateAPIView):
    queryset = models.Route.objects.all()
    serializer_class = serializers.RouteSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = serializers.RouteSerializer(queryset.filter(manager__user=self.request.user), many=True)
        return Response(serializer.data)


class DesignatedRouteReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.DesignatedRoute.objects.all()
    serializer_class = serializers.DesignatedRouteSerializer


class DesignatedRouteListCreateAPIView(ListCreateAPIView):
    queryset = models.DesignatedRoute.objects.all()
    serializer_class = serializers.DesignatedRouteSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = serializers.DesignatedRouteSerializer(queryset.filter(route__manager__user=self.request.user), many=True)
        return Response(serializer.data)