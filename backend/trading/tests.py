from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from .models import *

class PositionModelTest(TestCase):
    def setUp(self):
        # Set up a ticker instance with a specific price
        exchange = Exchange.objects.create(name="NYSE", url="https://nyse.com")
        self.ticker = Ticker.objects.create(exchange=exchange, symbol="AAPL", price=Decimal("150.00"))

    def test_position_bought_at_set_on_creation(self):
        # Create a Position with the Ticker instance
        position = Position.objects.create(ticker=self.ticker, amount=Decimal("10.00"))

        # Refresh the instance to get updated data
        position.refresh_from_db()
        
        # Assert that bought_at is set to the Ticker's current price
        self.assertEqual(position.bought_at, self.ticker.price)

    def test_bought_at_not_updated_on_save(self):
        # Create Position and set initial bought_at
        position = Position.objects.create(ticker=self.ticker, amount=Decimal("10.00"))
        position.refresh_from_db()

        # Change the Ticker's price
        self.ticker.price = Decimal("155.00")
        self.ticker.save()

        # Save Position again and check that bought_at has not changed
        position.save()
        position.refresh_from_db()
        self.assertEqual(position.bought_at, Decimal("150.00"))  # Should remain the original price

    def test_sell_function_updates_sold_at_and_ended_at(self):
        # Create Position and perform sell
        position = Position.objects.create(ticker=self.ticker, amount=Decimal("10.00"))

        before_sell_time = timezone.now()
        position.sell()

        # Refresh to get the latest data
        position.refresh_from_db()

        # Assert that sold_at is set to the current Ticker price and ended_at is set
        self.assertEqual(position.sold_at, self.ticker.price)
        self.assertIsNotNone(position.ended_at)
        self.assertAlmostEqual(position.ended_at, before_sell_time, delta=timezone.timedelta(seconds=1))
