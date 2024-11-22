from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from shelters.models import Shelter, Animal, CareTaker

SHELTER_LIST_URL = reverse("shelters:shelter-list")
SHELTER_CREATE_URL = reverse("shelters:shelter-create")
ANIMAL_LIST_URL = reverse("shelters:animal-list")
CARETAKER_LIST_URL = reverse("shelters:caretaker-list")
CARETAKER_CREATE_URL = reverse("shelters:caretaker-create")


class PublicShelterTests(TestCase):
    def setUp(self):
        self.shelter = Shelter.objects.create(
            name="Shelter One",
            location="Address One",
            contact_number="1234567890",
            capacity=100,
            current_animal_count=10,
        )

    def test_shelter_list_login_required(self):
        response = self.client.get(SHELTER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_shelter_detail_login_required(self):
        response = self.client.get(
            reverse("shelters:shelter-detail", args=[self.shelter.id])
        )
        self.assertNotEqual(response.status_code, 200)


class PrivateShelterTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(self.user)
        self.shelter = Shelter.objects.create(
            name="Shelter One",
            location="Address One",
            contact_number="1234567890",
            capacity=100,
            current_animal_count=10,
        )

    def test_shelter_list_view(self):
        response = self.client.get(SHELTER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Shelter One")

    def test_shelter_search(self):
        response = self.client.get(SHELTER_LIST_URL + "?name=Shelter One")
        self.assertContains(response, "Shelter One")


class PublicAnimalTests(TestCase):
    def setUp(self):
        self.shelter = Shelter.objects.create(
            name="Shelter Two",
            location="Address Two",
            contact_number="1234567890",
            capacity=100,
            current_animal_count=10,
        )
        self.animal = Animal.objects.create(
            name="Max",
            age=5,
            species="Dog",
            arrival_date=timezone.now().date(),
            shelter=self.shelter,
        )

    def test_animal_detail_login_required(self):
        response = self.client.get(
            reverse(
                "shelters:animal-detail",
                kwargs={"pk": self.animal.pk}
            )
        )
        self.assertNotEqual(response.status_code, 200)


class PrivateAnimalTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(self.user)
        self.shelter = Shelter.objects.create(
            name="Shelter Two",
            location="Address Two",
            contact_number="1234567890",
            capacity=100,
            current_animal_count=10,
        )
        self.animal = Animal.objects.create(
            name="Max",
            age=5,
            species="Dog",
            arrival_date=timezone.now().date(),
            shelter=self.shelter,
        )

    def test_animal_detail_view(self):
        response = self.client.get(
            reverse(
                "shelters:animal-detail",
                kwargs={"pk": self.animal.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Max")


class PublicCareTakerTests(TestCase):
    def setUp(self):
        self.caretaker = CareTaker.objects.create(
            username="public_caretaker", first_name="Public", last_name="User"
        )

    def test_login_required_for_caretaker_list(self):
        response = self.client.get(CARETAKER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_caretaker_detail_view(self):
        response = self.client.get(
            reverse(
                "shelters:caretaker-detail",
                args=[self.caretaker.id]
            )
        )
        self.assertNotEqual(response.status_code, 200)


class PrivateCareTakerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.force_login(self.user)
        self.caretaker1 = CareTaker.objects.create(
            username="caretaker1", first_name="First", last_name="User"
        )
        self.caretaker2 = CareTaker.objects.create(
            username="caretaker2", first_name="Second", last_name="User"
        )

    def test_retrieve_caretakers(self):
        response = self.client.get(CARETAKER_LIST_URL)
        caretakers = CareTaker.objects.all()
        self.assertEqual(
            list(response.context["caretaker_list"]),
            list(caretakers)
        )
        self.assertTemplateUsed(
            response, "shelters/caretaker_list.html"
        )

    def test_get_context_data_with_search_form(self):
        response = self.client.get(
            CARETAKER_LIST_URL, {"username": "caretaker1"}
        )
        search_form = response.context["search_form"]
        self.assertEqual(
            search_form.initial["username"], "caretaker1"
        )

    def test_get_queryset_with_search(self):
        response = self.client.get(
            CARETAKER_LIST_URL, {"username": "caretaker1"}
        )
        caretakers = CareTaker.objects.filter(
            username__icontains="caretaker1"
        )
        self.assertEqual(
            list(response.context["caretaker_list"]),
            list(caretakers)
        )
