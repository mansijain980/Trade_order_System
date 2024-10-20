import multiprocessing
import logging

# Configure logging
logger = logging.getLogger(__name__)

def start_order_receiver(orders_queue):
    from ..order_receiver import start_receiving_orders  # Relative import

    """Start the order receiver process, listening to Redis and adding orders to the queue."""
    start_receiving_orders(orders_queue)

def start_order_matching(orders_queue, trades_queue):
    from ..order_matching_process import OrderMatchingProcess  # Relative import

    """Start the order matching process, consuming from the order queue and adding to the trade queue."""
    matching_process = OrderMatchingProcess(trade_queue=trades_queue)
    while True:
        order_data = orders_queue.get()
        if order_data is None:  # Exit signal
            break
        matching_process.add_order(order_data)

def start_trade_sender(trade_queue):
    from ..trade_sender import send_trade  # Relative import

    """Start the trade sender process, consuming from the trade queue and sending trades to OMS."""
    while True:
        trade = trade_queue.get()
        if trade is None:  # Exit signal
            break
        send_trade(trade)

def start_tms():
    orders_queue = multiprocessing.Queue()
    trade_queue = multiprocessing.Queue()

    # Start processes
    receiver_process = multiprocessing.Process(target=start_order_receiver, args=(orders_queue,))
    matching_process = multiprocessing.Process(target=start_order_matching, args=(orders_queue, trade_queue))
    sender_process = multiprocessing.Process(target=start_trade_sender, args=(trade_queue,))

    receiver_process.start()
    matching_process.start()
    sender_process.start()

    # Join processes
    receiver_process.join()
    matching_process.join()
    sender_process.join()
