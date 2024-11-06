from django.shortcuts import render
from frontend.services.actions_service import ActionsService


def index(request):
    return render(request, "index.html")


def personal_actions_list(request):
    actions_service = ActionsService()
    pers_actions_list = actions_service.get_all_personal_actions()

    return render(request, "view_personal_actions.html", {"actions": pers_actions_list})


def available_actions_list(request):
    actions_service = ActionsService()
    avail_actions_list = actions_service.get_all_available_actions()

    return render(
        request, "view_available_actions.html", {"actions": avail_actions_list}
    )
