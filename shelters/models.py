from django.contrib.auth.models import AbstractUser
from django.db import models


class Shelter(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    capacity = models.IntegerField()
    current_animal_count = models.IntegerField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CareTaker(AbstractUser):
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    years_of_experience = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"
