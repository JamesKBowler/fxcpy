from ..logger import Log
log = Log().logger

MarketCondition = "5"

class Order(object):
    def __init__(self, order):
        log.debug("")
        self._order = order
        self._order.addRef()
        self._reject_amount = 0
        self._total_amount = 0
        self._state = "AwaitingExecution"
        self._result = "Executing"
        self._reject_message = None
        self._trades = []
        self._closed_trades = []
        self._orders = {}

    def __del__(self):
        log.debug("")
        for i in self._trades:
            i.release()
        for i in self._closed_trades:
            i.release()
        self._order.release()

    def _on_attach_to_order(self, order):
        """
        Attach order to the parent
        """
        order_id = order.getOrderID()
        self._orders[order_id] = order
        
    def _on_order_deleted(self, order):
        if order.getStatus() == 'R':
            log.debug("OrderRejected")
            self._state = "OrderRejected"
            self._reject_amount = order.getAmount()
            self._total_amount = order.getOriginAmount() - self._reject_amount
            if not self._reject_message and self.is_all_trades_received():
                self._set_result(True)

        elif order.getStatus() == 'C':
            log.debug("OrderCanceled")
            self._state = "OrderCanceled"
            self._reject_amount = order.getAmount()
            self._total_amount = order.getOriginAmount() - self._reject_amount
            if self.is_all_trades_received():
                self._set_result(False)
                
        elif  order.getStatus() == 'F':
            log.debug("OrderExecuted")
            self._reject_amount = 0
            self._total_amount = order.getOriginAmount()
            self._state = "OrderExecuted"
            if self.is_all_trades_received():
                self._set_result(True)
        else:
            # TODO
            log.debug("Order Status Not Impl:{}".format(order.getStatus()))

    def _on_trade_added(self, trade):
        log.debug("")
        trade.addRef()
        self._trades.append(trade)
        if (self._state == "OrderExecuted" or
            self._state == "OrderRejected" or
            self._state == "OrderCanceled"):
            if self.is_all_trades_received():
                self._set_result(True)

    def _on_closed_trade_added(self, closed_trade):
        log.debug("")
        closed_trade.addRef()
        self._closed_trades.append(closed_trade)
        if (self._state == "OrderExecuted" or
            self._state == "OrderRejected" or
            self._state == "OrderCanceled"):
            if self.is_all_trades_received():
                self._set_result(True)

    def _on_message_added(self, message):
        log.debug("")
        if (self._state == "OrderRejected" or
            self._state == "AwaitingExecution"):
            is_reject_message = self._check_and_store_message(message)
            if self._state == "OrderRejected" and is_reject_message:
                self._set_result(True)

    def _check_and_store_message(self, message):
        log.debug("")
        feature = message.getFeature()
        if feature == MarketCondition:
            text = message.getText()
            self._reject_message = text
            return True
        return False

    def _set_result(self, success):
        log.debug("")
        if success:
            if self._reject_amount == 0:
                self._result = "Executed"
            else:
                if len(self._trades) == 0 and len(self._closed_trades) == 0:
                    self._result = "FullyRejected"
                else:
                    self._result = "PartialRejected"
        else:
            self._result = "Canceled"

    def get_result(self):
        log.debug("")
        return self._result
    
    def get_order(self):
        log.debug("")
        self._order.addRef()
        return self._order

    def get_trades(self):
        log.debug("")
        for t in self._closed_trades:
            t.addRef()
        return self._trades

    def get_closed_trades(self):
        log.debug("")
        for c in self._closed_trades:
            c.addRef()
        return self._closed_trades

    def get_reject_amount(self):
        log.debug("")
        return self._reject_amount

    def get_reject_message(self):
        log.debug("")
        return self._reject_message

    def is_all_trades_received(self):
        log.debug("")
        if self._state == "AwaitingExecution":
            return False
        current_total_amount = 0
        for t in self._trades:
            current_total_amount += t.getAmount()
        for c in self._closed_trades:
            current_total_amount += c.getAmount()
        return current_total_amount == self._total_amount

    def _is_order_completed(self):
        log.debug("")
        return self._result != "Executing"
    
    def get_order_ids(self):
        """
        """
        log.debug("")
        order_ids = []
        try:
            main_id = self._order.getOrderID()
        except AttributeError:
            main_id = self._order.getOpenOrderID()
        order_ids.append(main_id)
        for order in self._orders.values():
            try:
                order_id = order.getOrderID()
            except AttributeError:
                order_id = order.getOpenOrderID
            order_ids.append(order_id)
        return order_ids