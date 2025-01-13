from django.urls import path

from .views import available_actions_list, personal_actions_list, action_info, buy_security, sell_security

urlpatterns = [
    path("personal-actions/", personal_actions_list, name="personal_actions"),
    path("available-actions/", available_actions_list, name="available_actions"),
    path("action/<str:symbol>.<str:exchange>/", action_info, name="action_info"),
    path("buy-security/", buy_security, name="buy_security"),
    path("sell-security/", sell_security, name="sell_security"),
]
