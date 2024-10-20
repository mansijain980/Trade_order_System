import redis
import json
import logging
import django
django.setup()
from trade_matching_service.models import Trade


# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Configure logging
logger = logging.getLogger(__name__)

def send_trade(trade):
    """Send the trade to Redis and save it in the database."""
    try:
        # Save the trade to the database
        trade_record = Trade(
            traded_quantity=trade['traded_quantity'],
            execution_price=trade['execution_price'],
            bid_order_id=trade['bid_order_id'],
            ask_order_id=trade['ask_order_id']
        )
        trade_record.save()  # Save the trade record

        # Send the trade to Redis
        trade_data_str = json.dumps(trade)
        print(trade_data_str)
        redis_client.rpush('trades_queue', trade_data_str)
        logger.info(f"Trade sent to Redis and saved in DB: {trade}")
    except Exception as e:
        logger.error(f"Error sending trade to Redis or saving to DB: {e}")
