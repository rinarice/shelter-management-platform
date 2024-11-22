from django import forms
from django.test import TestCase
from django.utils import timezone

from shelters.forms import (
    CareTakerCreationForm,
    CareTakerUpdateForm,
    AnimalForm,
    ShelterForm,
    CaretakerSearchForm,
    AnimalSearchForm,
    ShelterSearchForm,
)
from shelters.models import CareTaker, Shelter


class CareTakerCreationFormTest(TestCase):
    def test_caretaker_creation_form_valid(self):
        form_data = {
            "username": "testcaretaker",
            "password1": "testpass123",
            "password2": "testpass123",
            "first_name": "Test",
            "last_name": "Caretaker",
            "email": "test@example.com",
            "phone_number": "123456789",
            "address": "Test Address",
            "years_of_experience": 5,
        }
        form = CareTakerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_caretaker_creation_form_duplicate_username(self):
        CareTaker.objects.create(username="duplicateuser")
        form_data = {
            "username": "duplicateuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "email": "duplicate@example.com",
        }
        form = CareTakerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class CareTakerUpdateFormTest(TestCase):
    def test_caretaker_update_form_valid(self):
        form_data = {
            "username": "updatedcaretaker",
            "first_name": "Updated",
            "last_name": "Caretaker",
            "email": "updated@example.com",
            "phone_number": "987654321",
            "address": "Updated Address",
            "years_of_experience": 3,
        }
        form = CareTakerUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())


class AnimalFormTest(TestCase):
    def setUp(self):
        self.shelter = Shelter.objects.create(
            name="Test Shelter",
            location="Test Location",
            capacity=10,
            current_animal_count=5,
        )
        self.caretaker = CareTaker.objects.create_user(
            username="testcaretaker",
            password="password123",
        )

    def test_animal_form_valid(self):
        form_data = {
            "name": "Test Animal",
            "age": 3,
            "species": "Dog",
            "shelter": self.shelter.id,
            "caretakers": [self.caretaker.id],
            "arrival_date": "2023-01-01",
            "description": "Friendly and playful",
            "is_adopted": False,
        }
        form = AnimalForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_animal_form_future_arrival_date(self):
        form_data = {
            "name": "Buddy",
            "arrival_date": timezone.now().date() + timezone.timedelta(days=1),
        }
        form = AnimalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("arrival_date", form.errors)


class ShelterFormTest(TestCase):
    def test_shelter_form_valid(self):
        form_data = {
            "name": "Happy Shelter",
            "location": "123 Animal Street",
            "contact_number": "123456789",
            "capacity": 50,
            "current_animal_count": 10,
        }
        form = ShelterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_shelter_form_exceeds_capacity(self):
        form_data = {
            "capacity": 10,
            "current_animal_count": 15,
        }
        form = ShelterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("current_animal_count", form.errors)


class CaretakerSearchFormTest(TestCase):
    def test_caretaker_search_form_valid(self):
        form = CaretakerSearchForm(data={"username": "caretakername"})
        self.assertTrue(form.is_valid())

    def test_caretaker_search_form_empty(self):
        form = CaretakerSearchForm(data={})
        self.assertTrue(form.is_valid())


class AnimalSearchFormTest(TestCase):
    def test_animal_search_form_valid(self):
        form = AnimalSearchForm(data={"name": "Buddy"})
        self.assertTrue(form.is_valid())

    def test_animal_search_form_empty(self):
        form = AnimalSearchForm(data={})
        self.assertTrue(form.is_valid())


class ShelterSearchFormTest(TestCase):
    def test_shelter_search_form_valid(self):
        form = ShelterSearchForm(data={"name": "Happy Shelter"})
        self.assertTrue(form.is_valid())

    def test_shelter_search_form_empty(self):
        form = ShelterSearchForm(data={})
        self.assertTrue(form.is_valid())
