import yfinance as yf
from celery import shared_task

from .models import Ticker


@shared_task
def update_ticker_prices():
    tickers = Ticker.objects.all()
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker.symbol)
            price = stock.history(period="1d").tail(1)["Close"].iloc[0]
            ticker.price = price
            ticker.save()
            print(f"Updated {ticker.symbol} price to {ticker.price}")
        except Exception as e:
            print(f"Failed to update {ticker.symbol}: {e}")
