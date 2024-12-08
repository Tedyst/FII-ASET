from typing import Any
from django.db import models, transaction
from django.utils import timezone
from djmoney.models import fields as djmoney_fields
from simple_history.models import HistoricalRecords


class Account(models.Model):
    owner = models.OneToOneField("profiles.User", on_delete=models.CASCADE)
    balance = djmoney_fields.MoneyField(max_digits=14, decimal_places=2, default_currency="USD", default="0.00")  # type: ignore
    history: Any = HistoricalRecords()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    portfolio: "Portfolio"

    def __str__(self):
        return f"{self.owner.username}'s account"


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = djmoney_fields.MoneyField(max_digits=14, decimal_places=2)
    date = models.DateTimeField(auto_now=True)

    class Type(models.IntegerChoices):
        SELL = 0
        BUY = 1

    TYPES = ((Type.SELL, "Sell"), (Type.BUY, "Buy"))
    t_type = models.SmallIntegerField(choices=TYPES)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.account} - {Transaction.Type(self.t_type).label} - {self.amount} - transaction"


class Portfolio(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, default="Portfolio")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    positions: models.QuerySet["Position"]

    def value(self):
        return sum(
            [
                position.quantity * position.average_price
                for position in self.positions.all()
            ]
        )

    def __str__(self):
        return self.name


class Exchange(models.Model):
    name = models.CharField(max_length=64, db_index=True, unique=True)
    short_name = models.CharField(max_length=3, db_index=True, unique=True)
    url = models.URLField()

    def __str__(self):
        return self.name


class Security(models.Model):
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=16, db_index=True)
    price = djmoney_fields.MoneyField(max_digits=14, decimal_places=2)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    history = HistoricalRecords()
    users_purchased = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ["symbol", "exchange"]
        verbose_name_plural = "securities"
        indexes = [models.Index(fields=["symbol", "exchange"])]


class Position(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="positions"
    )
    quantity = models.DecimalField(max_digits=14, decimal_places=2)
    average_price = djmoney_fields.MoneyField(max_digits=14, decimal_places=2)
    security = models.ForeignKey(Security, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def value(self):
        return self.quantity * self.average_price

    def profit(self):
        return self.quantity * (self.security.price - self.average_price)

    def __str__(self):
        return f"{self.portfolio} - {self.security} - position"


class Order(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    security = models.ForeignKey(Security, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    class Type(models.IntegerChoices):
        SELL = 0
        BUY = 1

    TYPES = ((Type.SELL, "Sell"), (Type.BUY, "Buy"))
    t_type = models.SmallIntegerField(choices=TYPES)

    class Status(models.IntegerChoices):
        PENDING = 0
        FILLED = 1
        CANCELLED = 2

    STATUSES = (
        (Status.PENDING, "Pending"),
        (Status.FILLED, "Filled"),
        (Status.CANCELLED, "Cancelled"),
    )
    status = models.SmallIntegerField(choices=STATUSES, default=Status.PENDING)

    executed_at = models.DateTimeField(null=True)
    executed_price = djmoney_fields.MoneyField(
        max_digits=14, decimal_places=2, null=True
    )
    history = HistoricalRecords(inherit=True)

    @transaction.atomic
    def cancel(self):
        self.status = Order.Status.CANCELLED
        self.save()

    def can_fill(self):
        if self.t_type == Order.Type.BUY:
            return self.account.balance >= self.quantity * self.security.price
        elif self.t_type == Order.Type.SELL:
            position = self.account.portfolio.positions.get(security=self.security)
            return position.quantity >= self.quantity


class MarketOrder(Order):
    @transaction.atomic
    def fill(self):
        self.executed_at = timezone.now()
        self.status = Order.Status.FILLED

        if self.t_type == Order.Type.BUY:
            self.account.balance -= self.security.price * self.quantity
            self.account.save()

            position = Position(
                portfolio=self.account.portfolio,
                security=self.security,
                quantity=self.quantity,
                average_price=self.security.price,
            )
            position.save()
            Transaction.objects.create(
                account=self.account,
                amount=self.security.price * self.quantity,
                t_type=Transaction.Type.BUY,
            )
        elif self.t_type == Order.Type.SELL:
            self.account.balance += self.security.price * self.quantity
            self.account.save()

            position = self.account.portfolio.positions.get(security=self.security)
            position.quantity -= self.quantity
            position.save()

            Transaction.objects.create(
                account=self.account,
                amount=self.security.price * self.quantity,
                t_type=Transaction.Type.SELL,
            )
        self.save()


class LimitOrder(Order):
    limit_price = djmoney_fields.MoneyField(max_digits=14, decimal_places=2)
    expiration = models.DateTimeField()

    def can_fill(self):
        if self.t_type == Order.Type.BUY:
            return super().can_fill() and self.limit_price >= self.security.price
        elif self.t_type == Order.Type.SELL:
            return super().can_fill() and self.limit_price <= self.security.price

    def fill(self):
        raise NotImplementedError("Limit orders are not implemented yet")


class StopOrder(Order):
    stop_price = djmoney_fields.MoneyField(max_digits=14, decimal_places=2)
    expiration = models.DateTimeField()

    def can_fill(self):
        if self.t_type == Order.Type.BUY:
            return super().can_fill() and self.stop_price >= self.security.price
        elif self.t_type == Order.Type.SELL:
            return super().can_fill() and self.stop_price <= self.security.price

    def fill(self):
        self.executed_at = timezone.now()
        self.status = Order.Status.FILLED

        MarketOrder.objects.create(
            account=self.account,
            security=self.security,
            quantity=self.quantity,
            t_type=self.t_type,
        )
        self.save()


class ExternalMarketOrder(models.Model):
    order = models.ForeignKey(MarketOrder, on_delete=models.CASCADE)
    metadata = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order} - external order"

    def is_filled(self):
        return False


class ExternalMarketHolding(models.Model):
    external_market_order = models.ForeignKey(
        ExternalMarketOrder, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.external_market_order} - external holding"


class Tax(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    amount = djmoney_fields.MoneyField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction} - tax"
