from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from shelters.models import Animal, Shelter, CareTaker


class CareTakerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CareTaker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "phone_number",
            "address",
            "years_of_experience",
        )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CareTaker.objects.exclude(pk=self.instance.pk).filter(
                username=username).exists():
            raise forms.ValidationError(
                "A user with that username already exists.")
        return username


class CareTakerUpdateForm(forms.ModelForm):
    class Meta:
        model = CareTaker
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "address",
            "years_of_experience",
        ]


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
        return capacity

    def clean_current_animal_count(self):
        current_animal_count = self.cleaned_data.get("current_animal_count")
        capacity = self.cleaned_data.get("capacity")

        if capacity is not None and current_animal_count is not None:
            if current_animal_count > capacity:
                raise ValidationError(
                    "Current animal count cannot exceed capacity."
                )
        return current_animal_count


class CaretakerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by caretaker username"
            }
        )
    )

class AnimalSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by animal name"
            }
        )
    )

class ShelterSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by shelter name"
            }
        )
    )
