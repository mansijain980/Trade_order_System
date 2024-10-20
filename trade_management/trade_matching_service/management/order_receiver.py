import redis
import json
import pdb

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def start_receiving_orders(orders_queue):
    print(orders_queue)
    """Listen for orders in Redis and send them to the order matching process."""
    pubsub = redis_client.pubsub()
    pubsub.subscribe('order_channel')  # Subscribe to the Redis channel
    print(orders_queue)
    print("Listening for orders on Redis channel...")
  
    for message in pubsub.listen():
        print(message)  # Print the received message for debugging
        
        if message['type'] == 'message':
            try:
                # Decode message data from Redis
                message_data = message['data'].decode('utf-8')
                
                # Check if the message is a string that contains another JSON-encoded string
                if message_data.startswith('"') and message_data.endswith('"'):
                    # Remove the outer quotes and unescape the inner JSON string
                    message_data = json.loads(message_data)
                
                # Now check if it's a valid JSON string (after unescaping)
                if isinstance(message_data, str) and message_data.startswith('{') and message_data.endswith('}'):
                    # Decode the inner JSON string to a dictionary
                    order_data = json.loads(message_data)
                    print(f"Decoded order data: {order_data}")
                    
                    # Put the order into the multiprocessing queue as a dictionary
                    orders_queue.put(order_data)
                else:
                    print(f"Received non-JSON message: {message_data}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from Redis message: {e}")
            except Exception as e:
                print(f"Error processing order: {e}")
        else:
            # It's not a 'message' type, so ignore it (e.g., subscribe/unsubscribe messages)
            print(f"Received non-message type: {message['type']}, ignoring...")