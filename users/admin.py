from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("user",
                    "health_state",
                    "experience",
                    "car_type",
                    "car_max_load",
                    "pay_for_km",
                    "average_speed_per_hour",
                    "license_type",
                    "health_state",
                    )


@admin.register(models.Manager)
class ManagerAdmin(admin.ModelAdmin):
    pass

