from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from shelters.models import CareTaker, Animal, Shelter
from django.utils import timezone


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)

        self.shelter = Shelter.objects.create(
            name="Happy Paws",
            location="123 Bark St",
            contact_number="1234567890",
            capacity=50,
            current_animal_count=20
        )

        self.caretaker = CareTaker.objects.create_user(
            username="caretaker",
            password="testcaretaker",
            phone_number="1234567890",
            address="123 Paw Ave",
            years_of_experience=5,
        )

        self.animal = Animal.objects.create(
            name="Buddy",
            age=2,
            species="Dog",
            arrival_date=timezone.now().date(),
            is_adopted=False,
            shelter=self.shelter,
        )

    def test_caretaker_phone_number_listed(self):
        """
        Test that caretaker's phone number and years of experience are listed on the admin page.
        """
        url = reverse("admin:shelters_caretaker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.caretaker.phone_number)
        self.assertContains(res, self.caretaker.years_of_experience)

    def test_caretaker_detail_view_additional_fields(self):
        """
        Test that the phone number, address, and years of experience fields are displayed in caretaker detail view.
        """
        url = reverse("admin:shelters_caretaker_change",
                      args=[self.caretaker.id])
        res = self.client.get(url)
        self.assertContains(res, self.caretaker.phone_number)
        self.assertContains(res, self.caretaker.address)
        self.assertContains(res, self.caretaker.years_of_experience)

    def test_add_fieldsets_in_caretaker_admin(self):
        """
        Test that custom fields are in the add_fieldsets on the add caretaker page.
        """
        url = reverse("admin:shelters_caretaker_add")
        res = self.client.get(url)

        self.assertContains(res, 'name="username"')
        self.assertContains(res, 'name="phone_number"')
        self.assertContains(res, 'name="years_of_experience"')
        self.assertContains(res, 'name="address"')

    # Shelter Admin Tests
    def test_shelter_list_view_fields(self):
        """
        Test that shelter fields are listed on the admin list view.
        """
        url = reverse("admin:shelters_shelter_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.shelter.name)
        self.assertContains(res, self.shelter.location)
        self.assertContains(res, self.shelter.capacity)
        self.assertContains(res, self.shelter.current_animal_count)

    def test_shelter_search(self):
        """
        Test that shelter search works correctly for name and location fields.
        """
        url = reverse("admin:shelters_shelter_changelist") + "?q=Happy Paws"
        res = self.client.get(url)
        self.assertContains(res, self.shelter.name)

    # Animal Admin Tests
    def test_animal_list_view_fields(self):
        """
        Test that animal fields are listed on the admin list view.
        """
        url = reverse("admin:shelters_animal_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.animal.name)
        self.assertContains(res, self.animal.species)
        self.assertContains(res, self.animal.is_adopted)

    def test_animal_detail_view_species_and_shelter(self):
        """
        Test that animal detail view displays species and shelter.
        """
        url = reverse("admin:shelters_animal_change", args=[self.animal.id])
        res = self.client.get(url)
        self.assertContains(res, self.animal.species)
        self.assertContains(res, self.animal.shelter.name)

    def test_animal_filter_is_adopted(self):
        """
        Test that the is_adopted filter works on the animal admin page.
        """
        url = reverse(
            "admin:shelters_animal_changelist") + "?is_adopted__exact=0"
        res = self.client.get(url)
        self.assertContains(res, self.animal.name)
