from django.urls import path
from shelters.views import (
    index,
    ShelterListView,
    AnimalListView,
)

app_name = "shelters"

urlpatterns = [
    path("", index, name="index"),
    path("shelters/", ShelterListView.as_view(), name="shelter_list"),
    path("animals/", AnimalListView.as_view(), name="animal_list"),
]
