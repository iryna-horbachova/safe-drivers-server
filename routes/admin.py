from django.contrib import admin
from django.forms.widgets import TextInput

from django.contrib.gis.admin import OSMGeoAdmin

from . import models


class RouteAdmin(OSMGeoAdmin):
    list_display = ('manager', 'start_location', 'end_location', 'distance')
    readonly_fields = ('distance','start_location_string')


class DesignatedRouteAdmin(OSMGeoAdmin):
    pass


admin.site.register(models.Route, RouteAdmin)
admin.site.register(models.DesignatedRoute, DesignatedRouteAdmin)
