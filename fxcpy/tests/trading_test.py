from fxcpy.session_handler import SessionHandler
from fxcpy.settings import USER, PASS, URL, ENV
import time


session_handler = SessionHandler(USER, PASS, URL, ENV, True)
trading_commands = session_handler.get_trading_commands()
offers_table = session_handler.get_offers_table()
trades_table = session_handler.get_trades_table()
response_listener = session_handler.response_listener
def create_open_market_order_test():
    """
    Open 5 positions for EUR/USD.
    """
    master_valuemap = trading_commands.create_valuemap()
    for i in range(5):
        child_valuemap = trading_commands.create_open_market_order('1', 'B', 1)
        master_valuemap.appendChild(child_valuemap)
    trading_commands.execute_order(master_valuemap)
    response_listener.wait_events()

def create_order_open_test():
    """
    Open 5 positions for EUR/USD
    """
    master_valuemap = trading_commands.create_valuemap()
    bid = offers_table.get_bid('1')
    for i in range(5):
        child_valuemap = trading_commands.create_open_order(
            '1', 'B', 1, bid + 30.0 * offers_table.get_point_size('1')
        )
        master_valuemap.appendChild(child_valuemap)
    trading_commands.execute_order(master_valuemap)
    response_listener.wait_events()

def create_open_limit_order_test():
    """
    Create two limit orders
    """
    offer_id = '1'
    amount = 2
    master_valuemap = trading_commands.create_valuemap()
    ask = offers_table.get_ask(offer_id) + 100.0 * offers_table.get_point_size(offer_id)
    child_valuemap1 = trading_commands.create_open_limit_order(offer_id, 'B', amount, ask)
    master_valuemap.appendChild(child_valuemap1)
    bid = offers_table.get_ask(offer_id) - 100.0 * offers_table.get_point_size(offer_id)
    child_valuemap2 = trading_commands.create_open_limit_order(offer_id, 'S', amount, bid)
    master_valuemap.appendChild(child_valuemap2)
    trading_commands.execute_order(master_valuemap)
    response_listener.wait_events()

def create_stop_order_test():
    """
    Add stop loss to executed trades
    """
    master_valuemap = trading_commands.create_valuemap()
    # Scheisse! (drops coffee on the floor) we forgot to add stops!!!
    for trade_id, offer_id in trades_table.get_trade_ids().items():
        # For this demo we will match on symbol
        symbol = offers_table.get_instrument(offer_id)
        direction = trades_table.get_buysell(trade_id)
        if direction == 'B':
            # set stop 15 pips away
            rate = offers_table.get_ask(offer_id) - 15.0 * offers_table.get_point_size(offer_id)
            buysell = 'S'
        else: # direction == "S"
            rate = offers_table.get_bid(offer_id) + 15.0 * offers_table.get_point_size(offer_id)
            buysell = 'B'
        amount = trades_table.get_amount(trade_id)
        child_valuemap = trading_commands.create_stop_order(
            offer_id,
            trade_id,
            buysell,
            amount,
            rate,
            custom_id='Stop',
            time_in_force='GTC'
        )
        master_valuemap.appendChild(child_valuemap)
    trading_commands.execute_order(master_valuemap)
    response_listener.wait_events()

def create_limit_order_test():
    """
    Add limit to executed trades
    """
    master_valuemap = trading_commands.create_valuemap()
    # Scheisse! (drops coffee on the floor... again) we forgot to add limit orders!!!
    for trade_id, offer_id in trades_table.get_trade_ids().items():
        direction = trades_table.get_buysell(trade_id)
        if direction == 'B':
            # set limit 30 pips away
            rate = offers_table.get_ask(offer_id) + 30.0 * offers_table.get_point_size(offer_id)
            buysell = 'S'
        else: # direction == "S"
            rate = offers_table.get_bid(offer_id) - 30.0 * offers_table.get_point_size(offer_id)
            buysell = 'B'
        amount = trades_table.get_amount(trade_id)
        child_valuemap = trading_commands.create_limit_order(
            offer_id,
            trade_id,
            buysell,
            amount,
            rate,
            custom_id='Stop',
            time_in_force='GTC'
        )
        master_valuemap.appendChild(child_valuemap)
    trading_commands.execute_order(master_valuemap)
    response_listener.wait_events()
    
def create_close_market_order_test():
    """
    Close ALL trades
    """
    master_valuemap = trading_commands.create_valuemap()
    # None NET Order Clsoe Test
    for trade_id, offer_id in trades_table.get_trade_ids().items():
        direction = trades_table.get_buysell(trade_id)
        if direction == 'B':
            buysell = 'S'
        else: # direction == 'S'
            buysell = 'B'
        amount = trades_table.get_amount(trade_id)
        child_valuemap = trading_commands.create_close_market_order(
            offer_id,
            buysell,
            trade_id=trade_id,
            amount=amount,
            net_quantity='N'
        )
        master_valuemap.appendChild(child_valuemap)
    trading_commands.execute_order(master_valuemap)
    response_listener.wait_events()
    
def create_close_market_order_net_test():
    """
    NET Order Close Test
    """
    # Closing all LONG poistions for "EUR/USD"
    value_map = trading_commands.create_close_market_order('1', 'S')
    trading_commands.execute_order(value_map)
    response_listener.wait_events()
    
def create_open_market_order_and_attach_stoplimit_orders_test():
    """
    Wow thats a long name! 
    
    Creates 5 orders for EUR/USD, adds a stoploss and limit order
    then sends the order for execution.
    
    ie.. the stop and limit order are added before execution : )
    much safer
    
    """
    # Setup order to execute at market with stop and limit order
    offer_id = "1" # EUR/USD
    master_valuemap = trading_commands.create_valuemap()
    for i in range(5):
        child_valuemap = trading_commands.create_open_market_order(offer_id, "S", 1)
        master_valuemap.appendChild(child_valuemap)
        # 15 pip stop
        rate_stop = offers_table.get_bid(offer_id) + 15.0 * offers_table.get_point_size(offer_id)
        # 30 pip profit
        rate_limit = offers_table.get_bid(offer_id) - 30.0 * offers_table.get_point_size(offer_id)
        master_valuemap = trading_commands.attach_stoplimit_orders(
                i, # valuemap index
                master_valuemap,
                rate_stop=rate_stop, 
                rate_limit=rate_limit
        )
    trading_commands.execute_order(master_valuemap)
    response_listener.wait_events()


create_open_market_order_test()
print('create_open_market_order_test()')
time.sleep(2)
create_close_market_order_net_test()
print('create_close_market_order_net_test()')
time.sleep(2)
create_open_market_order_test()
print('create_open_market_order_test()')
time.sleep(2)
create_close_market_order_test()
print('create_close_market_order_test()')
time.sleep(2)
create_order_open_test()
print('create_order_open_test()')
time.sleep(2)
create_stop_order_test()
print('create_stop_order_test()')
time.sleep(2)
create_limit_order_test()
print('create_limit_order_test()')
time.sleep(2)
create_close_market_order_test()
print('create_close_market_order_test()')
time.sleep(2)
create_open_market_order_and_attach_stoplimit_orders_test()
print('create_open_market_order_and_attach_stoplimit_orders_test()')
time.sleep(2)
create_close_market_order_test()
print('create_close_market_order_test()')
time.sleep(2)
create_open_limit_order_test()
print('create_open_limit_order_test()')
time.sleep(2)
create_close_market_order_test()
print('create_close_market_order_test()')
time.sleep(3)
session_handler.logout()

