import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Portfolio, Position, Security, MarketOrder
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
        "csrf_token": request.COOKIES.get('csrftoken'),
    }

    # Returnează răspunsul împreună cu contextul completat
    return render(request, "action_info.html", context)


@login_required
@documents_approved_required
def buy_security(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        symbol = data.get('symbol')
        exchange = data.get('exchange')
        quantity = data.get('quantity')

        security = get_object_or_404(Security, symbol=symbol, exchange__short_name=exchange)
        account = request.user.account

        order = MarketOrder.objects.create(
            account=account,
            security=security,
            quantity=quantity,
            t_type=MarketOrder.Type.BUY,
            status=MarketOrder.Status.PENDING,
        )

        if order.can_fill():
            order.fill()
            return JsonResponse({'status': 'success', 'message': 'Buy order filled successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds or other issue.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@login_required
@documents_approved_required
def sell_security(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        symbol = data.get('symbol')
        exchange = data.get('exchange')
        quantity = data.get('quantity')

        security = get_object_or_404(Security, symbol=symbol, exchange__short_name=exchange)
        account = request.user.account

        order = MarketOrder.objects.create(
            account=account,
            security=security,
            quantity=quantity,
            t_type=MarketOrder.Type.SELL,
            status=MarketOrder.Status.PENDING,
        )

        if order.can_fill():
            order.fill()
            return JsonResponse({'status': 'success', 'message': 'Sell order filled successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient holdings or other issue.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
