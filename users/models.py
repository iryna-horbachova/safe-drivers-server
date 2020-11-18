from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.db import models


class User(AbstractUser):

    is_manager = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Manager(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} in {self.company}"


class Driver(models.Model):

    CAR_TYPE_CHOICES = (
        ("P", "Passenger"),
        ("C", "Cargo"),
    )

    LICENSE_CHOICES = (
        ("A", "Class A"),
        ("B", "Class B"),
        ("C", "Class C"),
        ("D", "Class D"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    manager = models.ForeignKey(Manager, related_name="driver_manager", on_delete=models.CASCADE)
    car_type = models.CharField(choices=CAR_TYPE_CHOICES, max_length=2, null=True, blank=True)
    car_max_load = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)], blank=True, null=True, default=None)
    experience = models.IntegerField(validators=[MinValueValidator(1)])
    pay_for_km = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)], blank=True,
                                       null=True, default=None)
    average_speed_per_hour = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(200)], blank=True,
                                       null=True, default=None)

    current_location = models.PointField(null=True, default=None)
    health_state = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True, default=None)
    license_type = models.CharField(choices=LICENSE_CHOICES, max_length=1, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


