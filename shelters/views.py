from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from shelters.models import Shelter, Animal, CareTaker


def index(request: HttpRequest) -> HttpResponse:
    num_shelters = Shelter.objects.count()
    num_animals = Animal.objects.count()
    num_caretakers = CareTaker.objects.count()

    context = {
        "num_shelters": num_shelters,
        "num_animals": num_animals,
        "num_caretakers": num_caretakers,
    }

    return render(request, "shelters/index.html", context)


class ShelterListView(generic.ListView):
    model = Shelter
    queryset = Shelter.objects.order_by("name")


class AnimalListView(generic.ListView):
    model = Animal
    queryset = Animal.objects.order_by("name")


class CareTakerListView(generic.ListView):
    model = CareTaker
    queryset = CareTaker.objects.order_by("first_name")
