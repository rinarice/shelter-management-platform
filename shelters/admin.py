from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from shelters.models import CareTaker, Animal, Shelter


@admin.register(CareTaker)
class CareTakerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "phone_number",
        "years_of_experience",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {
                "fields": ("phone_number", "address", "years_of_experience"),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "phone_number",
                    "address",
                    "years_of_experience",
                ),
            },
        ),
    )


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "capacity", "current_animal_count")
    search_fields = ("name", "location")


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "species", "is_adopted")
    search_fields = ("name", "species")
    list_filter = ("is_adopted", "species")
