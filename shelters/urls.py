from django.urls import path
from shelters.views import index

app_name = "shelters"

urlpatterns = [
    path("", index, name="index"),
]