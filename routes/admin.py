from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from . import models


class RouteAdmin(OSMGeoAdmin):
    list_display = ('manager', 'priority', 'load_type', 'distance')
    readonly_fields = ('distance',)


class DesignatedRouteAdmin(OSMGeoAdmin):
    list_display = ('route', 'driver', 'status', 'current_location')


admin.site.register(models.Route, RouteAdmin)
admin.site.register(models.DesignatedRoute, DesignatedRouteAdmin)
