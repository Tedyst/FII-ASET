from itertools import groupby
import logging
from django.db import transaction
import yfinance as yf
from celery import shared_task

from .models import (
    ExternalMarketHolding,
    ExternalMarketOrder,
    MarketOrder,
    Order,
    Security,
)


logger = logging.getLogger(__name__)


@shared_task(retry_backoff=True, max_retries=3, retry_jitter=True)
def update_security_price(security_id: int):
    security = Security.objects.get(pk=security_id)
    stock = yf.Ticker(security.symbol)
    price = stock.history(period="1d").tail(1)["Close"].iloc[0]
    security.price = price
    security.save()
    print(f"Updated {security.symbol} price to {security.price}")


@shared_task
def update_all_security_prices():
    for ticker in Security.objects.iterator():
        update_security_price.delay(ticker.pk)


@shared_task(retry_backoff=True, max_retries=3, retry_jitter=True)
@transaction.atomic
def market_making_market_orders():
    not_matched = []
    pending_market_orders = MarketOrder.objects.filter(status=Order.Status.PENDING)
    transactions_per_security = groupby(
        sorted(pending_market_orders, key=lambda x: x.security.pk),
        key=lambda x: x.security.pk,
    )

    # Try to match market orders first. If there is a SELL market order, try to match it with a BUY limit order. If either order is bigger than the other, fill the smaller order, cancel the bigger one, and create a new market order with the remaining quantity.
    for _, orders in transactions_per_security:
        orders = list(orders)
        buy_orders = [order for order in orders if order.t_type == Order.Type.BUY]
        sell_orders = [order for order in orders if order.t_type == Order.Type.SELL]

        for sell_order in sell_orders:
            if sell_order.status != Order.Status.PENDING:
                continue
            for buy_order in buy_orders:
                if buy_order.status != Order.Status.PENDING:
                    continue
                if sell_order.quantity == buy_order.quantity:
                    logger.info(
                        f"Matched {sell_order} with {buy_order} for {sell_order.security}"
                    )
                    sell_order.fill()
                    buy_order.fill()
                    break
                elif sell_order.quantity > buy_order.quantity:
                    logger.info(
                        f"Matched {buy_order} with {sell_order} for {sell_order.security}. Leftover quantity: {sell_order.quantity - buy_order.quantity}"
                    )
                    MarketOrder.objects.create(
                        account=sell_order.account,
                        security=sell_order.security,
                        t_type=Order.Type.SELL,
                        quantity=sell_order.quantity - buy_order.quantity,
                        status=Order.Status.PENDING,
                    )
                    sell_order.quantity = buy_order.quantity
                    sell_order.fill()
                    buy_order.fill()
                    break
                elif sell_order.quantity < buy_order.quantity:
                    logger.info(
                        f"Matched {sell_order} with {buy_order} for {sell_order.security}. Leftover quantity: {buy_order.quantity - sell_order.quantity}"
                    )
                    MarketOrder.objects.create(
                        account=buy_order.account,
                        security=buy_order.security,
                        t_type=MarketOrder.Type.BUY,
                        quantity=buy_order.quantity - sell_order.quantity,
                        status=MarketOrder.Status.PENDING,
                    )
                    buy_order.quantity = sell_order.quantity
                    sell_order.fill()
                    buy_order.fill()
                    break

    not_matched = MarketOrder.objects.filter(status=Order.Status.PENDING)
    for order in not_matched:
        ExternalMarketOrder.objects.create(order=order)


@shared_task(retry_backoff=True, max_retries=3, retry_jitter=True)
@transaction.atomic
def market_making():
    market_making_market_orders.delay()


@shared_task(retry_backoff=True, max_retries=3, retry_jitter=True)
@transaction.atomic
def external_market_making():
    orders = ExternalMarketOrder.objects.filter(order__status=Order.Status.PENDING)
    for order in orders:
        if order.is_filled():
            order.order.fill()
            ExternalMarketHolding.objects.create(external_market_order=order)
