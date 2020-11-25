from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.db import models
from users import models as users_models


class Route(models.Model):

    PRIORITY_CHOICES = (
        ("H", "High"),
        ("S", "Standard"),
        ("L", "Low")
    )

    LOAD_CHOICES = (
        ("P", "Passenger"),
        ("C", "Cargo"),
    )

    manager = models.ForeignKey(users_models.Manager, related_name="route_manager", on_delete=models.CASCADE)

    title = models.CharField(null=True, blank=True, max_length=100)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=1, null=True, blank=True)
    load_type = models.CharField(choices=LOAD_CHOICES, max_length=1, null=True, blank=True)
    load_quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)], blank=True, null=True, default=None)

    start_location = models.PointField()
    end_location = models.PointField()

    # distance between 2 locations in kms
    @property
    def distance(self):
        return round(self.start_location.distance(self.end_location) * 100)

    @property
    def is_in_progress(self):
        return DesignatedRoute.objects.filter(route_id=self.id).exists()

    def __str__(self):
        return f"{self.title}"


class DesignatedRoute(models.Model):

    STATUS_CHOICES = (
        ("N", "Not started"),
        ("I", "In progress"),
        ("F", "Finished")
    )

    route = models.ForeignKey(Route, related_name="route", on_delete=models.CASCADE)
    driver = models.ForeignKey(users_models.Driver, related_name="route_driver",
                               on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, null=True, blank=True)
    current_location = models.PointField(blank=True, null=True, default=None)
