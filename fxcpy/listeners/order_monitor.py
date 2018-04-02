from .order import Order

from ..logger import Log
log = Log().logger


class OrderMonitor(object):
    def __init__(self):
        log.debug("")
        self._monitors = {}

    def __del__(self):
        log.debug("")
        del self._monitors

    def _on_order_added(self, order):
        log.debug("")
        trade_id = order.getTradeID()
        if trade_id not in self._monitors:
            self._monitors[trade_id] = Order(order)
        else:
            self._monitors[trade_id]._on_attach_to_order(order)

    def _on_trade_added(self, trade):
        trade_id = trade.getTradeID()
        if trade_id in self._monitors:
            log.debug("")
            i = trade.getTradeID()
            self._monitors[i]._on_trade_added(trade)
        
    def _on_order_deleted(self, order):
        log.debug("")
        trade_id = order.getTradeID()
        if trade_id in self._monitors:
            self._monitors[trade_id]._on_order_deleted(order)

    def _on_message_added(self, trade_id, message):
        log.debug("")
        if trade_id in self._monitors:
            self._monitors[trade_id]._on_message_added(message)

    def _on_closed_trade_added(self, closed_trade):
        log.debug("")
        trade_id = closed_trade.getTradeID()
        if trade_id in self._monitors:
            self._monitors[trade_id]._on_closed_trade_added(closed_trade)

    def is_executed(self, trade_id):
        log.debug("")
        executed = False
        if trade_id in self._monitors:
            order = self._monitors[trade_id]
            if order._is_order_completed():
                executed = True
        return executed
        
    def get_monitors(self):
        log.debug("")
        return self._monitors