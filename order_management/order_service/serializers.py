from rest_framework import serializers
from .models import Order, Trade

class OrderSerializer(serializers.ModelSerializer):
    # Modify the serializer so that remaining_quantity is optional and handled automatically
    remaining_quantity = serializers.IntegerField(required=False)

    class Meta:
        model = Order
        fields = ['id', 'side', 'price', 'quantity', 'remaining_quantity', 'status']

    def create(self, validated_data):
        # Set remaining_quantity to the full quantity if not provided
        if 'remaining_quantity' not in validated_data:
            validated_data['remaining_quantity'] = validated_data['quantity']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle update logic if needed
        instance.remaining_quantity = validated_data.get('remaining_quantity', instance.remaining_quantity)
        return super().update(instance, validated_data)


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['id', 'side', 'price', 'quantity', 'remaining_quantity', 'average_traded_price', 'status', 'created_at']

#     def validate_price(self, value):
#         if value <= 0 or (value * 100) % 1 != 0:
#             raise serializers.ValidationError("Price must be greater than 0 and a multiple of 0.01")
#         return value

#     def validate_quantity(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Quantity must be greater than 0")
#         return value

class OrderModifySerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()

    def validate_price(self, value):
        if value <= 0 or (value * 100) % 1 != 0:
            raise serializers.ValidationError("Price must be greater than 0 and a multiple of 0.01")
        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['id', 'bid_order_id', 'ask_order_id', 'traded_quantity', 'execution_price', 'execution_timestamp']
