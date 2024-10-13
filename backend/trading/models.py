from django.db import models
from django.utils import timezone


class Exchange(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ticker(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TickerHistory(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)


class Position(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, db_index=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bought_at = models.DecimalField(max_digits=10, decimal_places=2)
    sold_at = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, db_index=True)

    def sell(self):
        self.sold_at = Ticker.objects.get(exchange=self.exchange, symbol=self.symbol).price
        self.ended_at = timezone.now()
        self.save()
