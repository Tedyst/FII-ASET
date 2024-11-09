import yfinance as yf
from celery import shared_task

from .models import Security


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
