from django.contrib import admin
from . import models


class HealthConditionAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.HealthCondition, HealthConditionAdmin)
