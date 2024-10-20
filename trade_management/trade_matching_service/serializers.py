from rest_framework import serializers
from .models import Order, Trade

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'side', 'price', 'quantity', 'remaining_quantity', 'average_traded_price', 'status', 'created_at']

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['id', 'bid_order_id', 'ask_order_id', 'traded_quantity', 'execution_price', 'execution_timestamp']
