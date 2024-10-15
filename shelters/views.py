from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

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
