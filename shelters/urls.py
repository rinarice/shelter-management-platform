from django.urls import path
from shelters.views import (
    index,
    ShelterListView,
    ShelterDetailView,
    AnimalListView,
    AnimalDetailView,
    CareTakerListView,
    CareTakerDetailView,
)

app_name = "shelters"

urlpatterns = [
    path("", index, name="index"),
    path(
        "shelters/",
        ShelterListView.as_view(),
        name="shelter_list"
    ),
    path(
        "shelters/<int:pk>",
        ShelterDetailView.as_view(),
        name="shelter_detail"
    ),
    path(
        "animals/",
        AnimalListView.as_view(),
        name="animal_list"
    ),
    path(
        "animals/<int:pk>/",
        AnimalDetailView.as_view(),
        name="animal_detail"
    ),
    path(
        "caretakers/",
        CareTakerListView.as_view(),
        name="caretaker_list"
    ),
    path(
        "caretakers/<int:pk>/",
        CareTakerDetailView.as_view(),
        name="caretaker_detail"
    ),
]
