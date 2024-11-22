from django.urls import path
from shelters.views import (
    index,
    ShelterListView,
    ShelterDetailView,
    ShelterCreateView,
    ShelterUpdateView,
    ShelterDeleteView,
    AnimalListView,
    AnimalDetailView,
    AnimalCreateView,
    AnimalUpdateView,
    AnimalDeleteView,
    CareTakerListView,
    CareTakerDetailView,
    CareTakerCreateView,
    CareTakerUpdateView,
    CareTakerDeleteView,
)

app_name = "shelters"

urlpatterns = [
    path("", index, name="index"),
    path(
        "shelters/",
        ShelterListView.as_view(),
        name="shelter-list"
    ),
    path(
        "shelters/<int:pk>/",
        ShelterDetailView.as_view(),
        name="shelter-detail"
    ),
    path(
        "shelters/create/",
        ShelterCreateView.as_view(),
        name="shelter-create"
    ),
    path(
        "shelters/<int:pk>/update/",
        ShelterUpdateView.as_view(),
         name="shelter-update"
    ),
    path(
        "shelters/<int:pk>/delete/",
        ShelterDeleteView.as_view(),
         name="shelter-delete"
    ),
    path(
        "animals/",
        AnimalListView.as_view(),
        name="animal-list"
    ),
    path(
        "animals/<int:pk>/",
        AnimalDetailView.as_view(),
        name="animal-detail"
    ),
    path(
        "animals/create/",
        AnimalCreateView.as_view(),
        name="animal-create"
    ),
    path(
        "animals/<int:pk>/update/",
        AnimalUpdateView.as_view(),
        name="animal-update"
    ),
    path(
        "animals/<int:pk>/delete/",
        AnimalDeleteView.as_view(),
        name="animal-delete"
    ),
    path(
        "caretakers/",
        CareTakerListView.as_view(),
        name="caretaker-list"
    ),
    path(
        "caretakers/<int:pk>/",
        CareTakerDetailView.as_view(),
        name="caretaker-detail"
    ),
    path(
        "caretakers/create/",
        CareTakerCreateView.as_view(),
        name="caretaker-create"
    ),
    path(
        "caretakers/<int:pk>/update/",
        CareTakerUpdateView.as_view(),
        name="caretaker-update"
    ),
    path(
        "caretakers/<int:pk>/delete/",
        CareTakerDeleteView.as_view(),
        name="caretaker-delete"
    ),
]
