from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from shelters.models import Animal, Shelter


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = "__all__"
        widgets = {
            "caretakers": forms.CheckboxSelectMultiple(),
        }

    def clean_arrival_date(self):
        arrival_date = self.cleaned_data.get("arrival_date")
        if arrival_date and arrival_date > timezone.now().date():
            raise ValidationError("Arrival date cannot be in the future.")
        return arrival_date


class ShelterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = "__all__"

    def clean_capacity(self):
        capacity = self.cleaned_data.get("capacity")
        current_animal_count = self.cleaned_data.get("current_animal_count")
        if capacity is not None and current_animal_count is not None:
            if capacity < current_animal_count:
                raise ValidationError(
                    "Capacity cannot be less than the current animal count."
                )
        return capacity
