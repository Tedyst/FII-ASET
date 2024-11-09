import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Portfolio, Position, Security

logger = logging.getLogger(__name__)


@login_required
def personal_actions_list(request) -> HttpResponse:
    positions = (
        Position.objects.prefetch_related("security")
        .filter(portfolio__account__owner=request.user)
        .all()
    )
    positions_agg = {}
    for position in positions:
        if position.security not in positions_agg:
            positions_agg[position.security] = {
                "security": position.security,
                "quantity": 0,
                "average_price": 0,
                "profit": 0,
            }
        positions_agg[position.security]["quantity"] += position.quantity
        positions_agg[position.security]["average_price"] += (
            position.average_price * position.quantity
        )
        positions_agg[position.security]["profit"] += position.profit()

    for _, data in positions_agg.items():
        data["average_price"] /= data["quantity"]

    return render(
        request, "view_personal_actions.html", {"positions": positions_agg.values()}
    )


def available_actions_list(request):
    return render(
        request, "view_available_actions.html", {"securities": Security.objects.all()}
    )


def action_info(request, action_pk: int):
    return render(
        request,
        "action_info.html",
        {"security": get_object_or_404(Security, pk=action_pk)},
    )
