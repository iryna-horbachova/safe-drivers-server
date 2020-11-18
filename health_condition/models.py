from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.db import models
from users import models as users_models


class HealthCondition(models.Model):
    driver = models.ForeignKey(users_models.Driver, related_name="driver_condition", on_delete=models.CASCADE)

    heart_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    body_temperature = models.IntegerField(validators=[MinValueValidator(34), MaxValueValidator(40)])
    respiration_rate_per_minute = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(25)])
    blood_pressure_systolic = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(200)])
    blood_pressure_diastolic = models.IntegerField(validators=[MinValueValidator(80), MaxValueValidator(140)])
    blood_oxygen_level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    blood_alcohol_content = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    drugs_alcohol_content = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)])

    datetime = models.DateTimeField(auto_now_add=True)