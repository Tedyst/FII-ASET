from django.urls import path

from . import views
from .views import available_actions_list, index, personal_actions_list

urlpatterns = [
    path("", index, name="index"),
    path("personal-actions/", personal_actions_list, name="personal_actions"),
    path("available-actions/", available_actions_list, name="available_actions"),
]
