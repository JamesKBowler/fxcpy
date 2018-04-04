def print_order_monitor(monitor):
    """
    This is just print test, but its likely to be a Queue of some sort.
    """
    trade_id = monitor._order.getTradeID()
    print("TradeID {}".format(trade_id))
