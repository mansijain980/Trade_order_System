from django.db import models
from django.utils import timezone

class Order(models.Model):
    SIDE_CHOICES = (
        (1, 'Buy'),
        (-1, 'Sell'),
    )
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('partially_filled', 'Partially Filled'),
        ('filled', 'Filled'),
        ('cancelled', 'Cancelled'),
    )

    side = models.IntegerField(choices=SIDE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    remaining_quantity = models.IntegerField()  # To track partially traded orders
    average_traded_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}: {'Buy' if self.side == 1 else 'Sell'} {self.quantity} @ {self.price}"

class Trade(models.Model):
    bid_order_id = models.IntegerField()
    ask_order_id = models.IntegerField()
    traded_quantity = models.IntegerField()
    execution_price = models.DecimalField(max_digits=10, decimal_places=2)
    execution_timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Trade {self.id}: {self.traded_quantity} units @ {self.execution_price}"
