import logging
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import MarketOrder, Order, Portfolio, Position, Security
import json
from profiles.decorators import documents_approved_required

logger = logging.getLogger(__name__)


@login_required
@documents_approved_required
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


@documents_approved_required
def available_actions_list(request):
    return render(
        request, "view_available_actions.html", {"securities": Security.objects.all()}
    )


@documents_approved_required
def action_info(request, symbol: str, exchange: str):
    # Găsim obiectul Security folosind get_object_or_404
    security = get_object_or_404(
        Security.objects.prefetch_related("exchange"),
        symbol=symbol,
        exchange__short_name=exchange,
    )

    # Obține istoricul prețurilor (cele mai recente 7 modificări)
    price_history = security.history.filter(price__isnull=False).order_by(
        "-history_date"
    )[:100]

    user_orders = MarketOrder.objects.filter(
        security=security, account__owner=request.user
    ).all()

    # Pregătește datele pentru grafic în format JSON
    historical_prices = [
        float(record.price.amount) for record in price_history
    ]  # JSON serializat
    historical_dates = [
        record.history_date.strftime("%d %B") for record in price_history
    ]  # JSON serializat

    if len(price_history) >= 2:
        last_price = price_history[0].price.amount
        previous_price = price_history[1].price.amount
        price_difference = last_price - previous_price
    else:
        price_difference = None

    if len(historical_prices) >= 2:
        # Calculăm diferența procentuală față de ziua precedentă
        price_difference_percentage = (
            (historical_prices[0] - historical_prices[1]) / historical_prices[1]
        ) * 100
    else:
        price_difference_percentage = None  # Dacă nu există suficiente date

    historical_prices.reverse()  # Inversează lista prețurilor
    historical_dates.reverse()  # Inversează lista datelor
    users_purchased = security.users_purchased
    # Contextul care include securitatea și datele istorice pentru grafic
    context = {
        "security": security,
        "historical_prices": historical_prices,  # Date JSON serializate
        "historical_dates": historical_dates,  # Date JSON serializate
        "price_difference": price_difference,
        "price_difference_percentage": price_difference_percentage,
        "users_purchased": users_purchased,
        "orders": user_orders,
    }

    return render(request, "action_info.html", context)


class CreateOptionForm(forms.Form):
    security = forms.IntegerField()
    quantity = forms.IntegerField()
    price = forms.IntegerField(required=False)
    type = forms.CharField(required=False)
    order_type = forms.CharField(required=False)


@login_required
def create_option(request):
    if request.method == "POST":
        form = CreateOptionForm(request.POST)
        if form.is_valid():
            account = request.user.account
            security = Security.objects.get(id=form.cleaned_data["security"])
            quantity = form.cleaned_data["quantity"]
            order_type = form.cleaned_data["type"]
            order = MarketOrder.objects.create(
                account=account,
                security=security,
                quantity=quantity,
                t_type=(
                    MarketOrder.Type.BUY
                    if order_type == "buy"
                    else MarketOrder.Type.SELL
                ),
            )
            order.save()
            return redirect(
                "action_info",
                symbol=security.symbol,
                exchange=security.exchange.short_name,
            )
        return HttpResponse(form.errors)
    return HttpResponse("Invalid form data")
