from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from shelters.models import Shelter, Animal, CareTaker


@login_required
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


class ShelterListView(LoginRequiredMixin, generic.ListView):
    model = Shelter
    queryset = Shelter.objects.order_by("name")


class ShelterDetailView(LoginRequiredMixin, generic.DetailView):
    model = Shelter


class AnimalListView(LoginRequiredMixin, generic.ListView):
    model = Animal
    queryset = Animal.objects.order_by("name")


class AnimalDetailView(LoginRequiredMixin, generic.DetailView):
    model = Animal


class CareTakerListView(LoginRequiredMixin, generic.ListView):
    model = CareTaker
    queryset = CareTaker.objects.order_by("first_name")


class CareTakerDetailView(LoginRequiredMixin, generic.DetailView):
    model = CareTaker
