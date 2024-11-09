import random
import faker

from django.db import transaction
from djmoney.money import Money

from trading.models import Exchange, Account, Transaction, Portfolio, Security, Position
from profiles.models import User


@transaction.atomic
def run():
    f = faker.Faker()
    exchange = Exchange.objects.create(name=f.name() + " Exchange", url=f.url())
    for user in User.objects.all():
        account, _ = Account.objects.get_or_create(owner=user)
        portfolio = Portfolio.objects.create(account=account)

        for _ in range(10):
            security_name = f.company()
            security_symbol = security_name[:3].upper()
            if Security.objects.filter(
                symbol=security_symbol, exchange=exchange
            ).exists():
                security = Security.objects.get(
                    symbol=security_symbol, exchange=exchange
                )
            else:
                security = Security.objects.create(
                    name=security_name,
                    symbol=security_symbol,
                    price=Money(random.random() * 100, "USD"),
                    exchange=exchange,
                )

            for _ in range(random.randint(0, 10)):
                position = Position.objects.create(
                    security=security,
                    portfolio=portfolio,
                    quantity=random.random() * 100,
                    average_price=Money(random.random() * 100, "USD"),
                )

                Transaction.objects.create(
                    account=account,
                    amount=position.quantity * position.average_price,
                    t_type=Transaction.Type.BUY,
                )

                if random.random() > 0.5:
                    t = Transaction.objects.create(
                        account=account,
                        amount=Money(random.random() * 100, "USD"),
                        t_type=Transaction.Type.BUY,
                    )
                    Transaction.objects.create(
                        account=account,
                        amount=t.amount,
                        t_type=Transaction.Type.SELL,
                    )
