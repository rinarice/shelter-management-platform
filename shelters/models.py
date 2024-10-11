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
