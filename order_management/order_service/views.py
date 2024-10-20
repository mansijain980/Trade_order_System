from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, Trade
from .serializers import OrderSerializer, OrderModifySerializer, TradeSerializer
import redis
import json

import logging

# Set up logging
logger = logging.getLogger(__name__)


def add_order_to_redis_queue(order_data):
    # Convert Python dict to JSON string before pushing to Redis
    order_data_str = json.dumps(order_data)
    redis_client.rpush('orders_queue', order_data_str)  # Push to Redis queue
    logger.info(f"Order added to Redis queue: {order_data_str}")

    # Publish the order to 'order_channel' so TMS can process it
    redis_client.publish('order_channel', order_data_str)
    logger.info(f"Order published to Redis channel: {order_data_str}")


# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Test Redis connection
try:
    redis_client.ping()
    print("Redis is connected")
except redis.exceptions.ConnectionError:
    print("Failed to connect to Redis")




# # Helper function to add order to Redis queue
# def add_order_to_redis_queue(order_data):
#     order_data_str = json.dumps(order_data)

#     redis_client.rpush('orders_queue', order_data_str)

# Helper function to notify TMS to perform matching
def notify_tms():
    redis_client.publish('order_channel', 'New order added or updated')

# Place order [POST]
@api_view(['POST'])
def place_order(request):
    data = request.data
    serializer = OrderSerializer(data=data)

    if serializer.is_valid():
        order = serializer.save()
        # Prepare order data for Redis
        order_data = {
            'order_id': order.id,
            'side': order.side,
            'price': float(order.price),
            'quantity': order.quantity,
        }
        print(type(order_data))
        order_data_str = json.dumps(order_data)  # Use JSON format for consistency
        add_order_to_redis_queue(order_data_str)
        logger.info(f"Order added to Redis queue: {order_data}")
        notify_tms()  # Notify the TMS to match orders
        return Response({'order_id': order.id, 'status': 'Order placed in Redis queue'}, status=201)

    return Response(serializer.errors, status=400)

# Modify order [PUT]
@api_view(['PUT'])
def modify_order(request):
    order_id = request.data.get('order_id')
    updated_price = request.data.get('updated_price')

    if not order_id or updated_price is None:
        return Response({'success': False, 'message': 'order_id and updated_price are required'}, status=400)

    order = get_object_or_404(Order, id=order_id)

    # Update order price
    order.price = updated_price
    order.save()

    # Prepare updated order data for Redis
    updated_order_data = {
        'order_id': order.id,
        'side': order.side,
        'price': float(order.price),
        'quantity': order.quantity,
    }

    # Notify TMS about the updated order
    notify_tms()
    add_order_to_redis_queue(updated_order_data)

    return Response({'success': True, 'message': 'Order modified successfully'}, status=200)

# Cancel order [DELETE]
@api_view(['DELETE'])
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status in ['open', 'partially_filled']:
        # Cancel remaining quantity
        order.delete()
        order.remaining_quantity = 0
        order.status = 'cancelled'
     

        # Notify TMS about the cancellation
        notify_tms()

        return Response({'success': True, 'message': 'Order cancelled'}, status=200)

    return Response({'success': False, 'message': 'Order already completed or cancelled'}, status=400)

# Fetch order details [GET]
@api_view(['GET'])
def fetch_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=200)

# Fetch all orders [GET]
@api_view(['GET'])
def fetch_all_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=200)

# Fetch all trades [GET]
@api_view(['GET'])
def fetch_all_trades(request):
    trades = Trade.objects.all()
    serializer = TradeSerializer(trades, many=True)
    return Response(serializer.data, status=200)

# Fetch a single trade by ID [GET]
@api_view(['GET'])
def fetch_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id)
    serializer = TradeSerializer(trade)
    return Response(serializer.data, status=200)
