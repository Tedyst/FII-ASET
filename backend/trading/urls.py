from django.urls import path

from .views import available_actions_list, personal_actions_list

urlpatterns = [
    path("personal-actions/", personal_actions_list, name="personal_actions"),
    path("available-actions/", available_actions_list, name="available_actions"),
]
