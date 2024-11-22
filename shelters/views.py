from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from shelters.forms import (
    AnimalForm,
    CareTakerCreationForm,
    ShelterForm,
    ShelterSearchForm,
    AnimalSearchForm,
    CaretakerSearchForm, CareTakerUpdateForm
)
from shelters.models import Shelter, Animal, CareTaker


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_shelters = Shelter.objects.count()
    num_animals = Animal.objects.count()
    num_caretakers = CareTaker.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_shelters": num_shelters,
        "num_animals": num_animals,
        "num_caretakers": num_caretakers,
        "num_visits": num_visits + 1,
    }

    return render(request, "shelters/index.html", context)


class ShelterListView(LoginRequiredMixin, generic.ListView):
    model = Shelter
    context_object_name = "shelter_list"
    template_name = "shelters/shelter_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ShelterSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ShelterSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class ShelterDetailView(LoginRequiredMixin, generic.DetailView):
    model = Shelter


class ShelterCreateView(generic.CreateView):
    model = Shelter
    form_class = ShelterForm
    success_url = reverse_lazy("shelters:shelter-list")


class ShelterUpdateView(generic.UpdateView):
    model = Shelter
    form_class = ShelterForm
    success_url = reverse_lazy("shelters:shelter-list")


class ShelterDeleteView(generic.DeleteView):
    model = Shelter
    success_url = reverse_lazy("shelters:shelter-list")


class AnimalListView(LoginRequiredMixin, generic.ListView):
    model = Animal
    context_object_name = "animal_list"
    template_name = "shelters/animal_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = AnimalSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = AnimalSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class AnimalDetailView(LoginRequiredMixin, generic.DetailView):
    model = Animal

    def post(self, request, *args, **kwargs):
        animal = self.get_object()
        action = request.POST.get("action")

        if action == "start_caring":
            animal.caretakers.add(request.user)
        elif action == "stop_caring":
            animal.caretakers.remove(request.user)

        return redirect("shelters:animal-detail", pk=animal.pk)


class AnimalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Animal
    form_class = AnimalForm
    success_url = reverse_lazy("shelters:animal-list")


class AnimalUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Animal
    form_class = AnimalForm
    success_url = reverse_lazy("shelters:animal-list")


class AnimalDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Animal
    success_url = reverse_lazy("shelters:animal-list")


class CareTakerListView(LoginRequiredMixin, generic.ListView):
    model = CareTaker
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CareTakerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CaretakerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = CaretakerSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset

class CareTakerDetailView(LoginRequiredMixin, generic.DetailView):
    model = CareTaker


class CareTakerCreateView(LoginRequiredMixin, generic.CreateView):
    model = CareTaker
    form_class = CareTakerCreationForm
    success_url = reverse_lazy("shelters:caretaker-list")


class CareTakerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CareTaker
    form_class = CareTakerUpdateForm
    success_url = reverse_lazy("shelters:caretaker-list")


class CareTakerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = CareTaker
    success_url = reverse_lazy("shelters:caretaker-list")
