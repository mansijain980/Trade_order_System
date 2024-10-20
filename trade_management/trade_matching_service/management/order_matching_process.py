import heapq
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Order:
    def __init__(self, order_id, side, price, quantity):
        self.order_id = order_id
        self.side = side  # 1 for buy, -1 for sell
        self.price = price
        self.quantity = quantity
        self.remaining_quantity = quantity

    def __lt__(self, other):
        if self.price == other.price:
            return self.order_id < other.order_id
        return self.price < other.price if self.side == -1 else self.price > other.price

class OrderMatchingProcess:
    def __init__(self, trade_queue=None):
        # Min-heap for sell orders (ask)
        self.sell_orders = []
        # Max-heap for buy orders (bid)
        self.buy_orders = []
        self.orders = {}  # To keep track of orders by ID
        self.trades = []  # To record trades
        self.trade_queue = trade_queue  # Queue to send trades to the trade sender

    def add_order(self, order_data):
        """Adds a new order to the order book and attempts to match it."""
        order = Order(
            order_id=order_data['order_id'],
            side=order_data['side'],
            price=order_data['price'],
            quantity=order_data['quantity']
        )
        logger.debug(f"Adding order: {order.__dict__}")
        self.orders[order.order_id] = order

        if order.side == 1:  # Buy order
            heapq.heappush(self.buy_orders, order)
            self.match_orders(order)
        else:  # Sell order
            heapq.heappush(self.sell_orders, order)
            self.match_orders(order)

    def match_orders(self, incoming_order):
        """Matches incoming orders against the existing order book."""
        logger.debug(f"Matching incoming order: {incoming_order.__dict__}")
        
        while incoming_order.remaining_quantity > 0:
            logger.debug(f"Buy Orders: {[o.__dict__ for o in self.buy_orders]}, Sell Orders: {[o.__dict__ for o in self.sell_orders]}")

            if incoming_order.side == 1:  # Buy order
                if not self.sell_orders or incoming_order.price < self.sell_orders[0].price:
                    break  # No match possible
                
                best_ask = self.sell_orders[0]  # Get the best ask

                # Match orders
                trade_quantity = min(incoming_order.remaining_quantity, best_ask.remaining_quantity)
                traded_price = best_ask.price
                trade = self.create_trade(trade_quantity, traded_price, incoming_order.order_id, best_ask.order_id)
                
                # Log the trade
                logger.debug(f"Trade executed: {trade}")
                self.trades.append(trade)
                if self.trade_queue:
                    self.trade_queue.put(trade)  # Push the trade to the queue
                
                # Update the quantities
                incoming_order.remaining_quantity -= trade_quantity
                best_ask.remaining_quantity -= trade_quantity

                # If the best ask is fully filled, remove it
                if best_ask.remaining_quantity == 0:
                    heapq.heappop(self.sell_orders)
                    del self.orders[best_ask.order_id]

            else:  # Sell order
                if not self.buy_orders or incoming_order.price > self.buy_orders[0].price:
                    break  # No match possible

                best_bid = self.buy_orders[0]  # Get the best bid

                # Match orders
                trade_quantity = min(incoming_order.remaining_quantity, best_bid.remaining_quantity)
                traded_price = best_bid.price
                trade = self.create_trade(trade_quantity, traded_price, best_bid.order_id, incoming_order.order_id)
                
                # Log the trade
                logger.debug(f"Trade executed: {trade}")
                self.trades.append(trade)
                if self.trade_queue:
                    self.trade_queue.put(trade)  # Push the trade to the queue
                
                # Update the quantities
                incoming_order.remaining_quantity -= trade_quantity
                best_bid.remaining_quantity -= trade_quantity

                # If the best bid is fully filled, remove it
                if best_bid.remaining_quantity == 0:
                    heapq.heappop(self.buy_orders)
                    del self.orders[best_bid.order_id]

        # If incoming_order is partially filled, keep it in the respective order book
        if incoming_order.remaining_quantity > 0:
            logger.debug(f"Order with remaining quantity stays in the book: {incoming_order.__dict__}")

    def create_trade(self, quantity, price, bid_order_id, ask_order_id):
        """Helper method to create a trade dictionary."""
        return {
            'traded_quantity': quantity,
            'execution_price': price,
            'bid_order_id': bid_order_id,
            'ask_order_id': ask_order_id
        }

    def get_trades(self):
        """Returns all trades that have taken place."""
        return self.trades

    def get_order_book(self):
        """Returns a snapshot of the current order book."""
        buy_orders = [(order.order_id, order.price, order.quantity, order.remaining_quantity) for order in self.buy_orders]
        sell_orders = [(order.order_id, order.price, order.quantity, order.remaining_quantity) for order in self.sell_orders]
        logger.debug(f"Current order book - Buy Orders: {buy_orders}, Sell Orders: {sell_orders}")
        print(buy_orders, sell_orders)
        return {
            'buy_orders': buy_orders,
            'sell_orders': sell_orders,
        }
