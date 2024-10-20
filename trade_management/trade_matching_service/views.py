# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Trade
# from .serializers import TradeSerializer
# from .order_receiver import start_receiving_orders
# from .trade_sender import send_trade  # Assuming this is the function to send trades
# import threading



# # Fetch all trades [GET]
# @api_view(['GET'])
# def fetch_all_trades(request):
#     """Returns all trades taken place."""
#     trades = Trade.objects.all()
#     serializer = TradeSerializer(trades, many=True)
#     return Response(serializer.data, status=200)

# Add more view functions as needed for your application
# views.py

from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def fetch_all_trades(request):
    """Returns all trades that have taken place."""
    from .models import Trade  # Move import here

    try:
        trades = Trade.objects.all()
        data = [{'id': trade.id, 'quantity': trade.traded_quantity} for trade in trades]
        return JsonResponse(data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
