from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from shelters.models import Shelter, Animal

User = get_user_model()

class ModelTests(TestCase):
    def test_shelter_str(self):
        shelter = Shelter.objects.create(
            name="Happy Paws",
            location="123 Bark St",
            contact_number="1234567890",
            capacity=50,
            current_animal_count=20,
        )
        self.assertEqual(str(shelter), "Happy Paws")

    def test_caretaker_str(self):
        caretaker = User.objects.create_user(
            username="caretaker1",
            password="test123",
            first_name="John",
            last_name="Doe",
            email="caretaker@example.com",
            phone_number="1234567890",
            years_of_experience=5,
        )
        self.assertEqual(str(caretaker), "caretaker1 (John Doe)")

    def test_animal_str(self):
        shelter = Shelter.objects.create(
            name="Happy Tails",
            location="789 Meow Ln",
            contact_number="0987654321",
            capacity=100,
            current_animal_count=20,
        )
        animal = Animal.objects.create(
            name="Buddy",
            age=2,
            species="Dog",
            arrival_date=timezone.now(),
            shelter=shelter,
        )
        self.assertEqual(str(animal), "Buddy")

    def test_create_caretaker_with_phone_and_experience(self):
        username = "caretaker2"
        password = "test456"
        caretaker = User.objects.create_user(
            username=username,
            password=password,
            phone_number="0987654321",
            years_of_experience=3,
        )
        self.assertEqual(caretaker.username, username)
        self.assertEqual(caretaker.phone_number, "0987654321")
        self.assertEqual(caretaker.years_of_experience, 3)
        self.assertTrue(caretaker.check_password(password))
