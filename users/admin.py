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
                    "license_type"
                    )


@admin.register(models.Manager)
class ManagerAdmin(admin.ModelAdmin):
    pass

