# The MIT License (MIT)
#
# Copyright (c) 2018 James K Bowler, Data Centauri Ltd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from forexconnect import CTableListener
from forexconnect import (
    O2GTable,
    IO2GAccountsTable, 
    IO2GOrdersTable, 
    IO2GTradesTable, 
    IO2GMessagesTable,
    IO2GClosedTradesTable,
    IO2GAccountTableRow, 
    IO2GOrderRow, 
    IO2GTradeRow,
    IO2GClosedTradeRow,
    IO2GMessageRow,
    O2GTableUpdateType
)

from forexconnect import (
    Trades,
    Orders,
    ClosedTrades,
    Messages,
    Accounts
)

from .order_printer import print_order_monitor

from .order_monitor import OrderMonitor

from eventfd import EventFD
from . import Counter

from ..logger import Log
log = Log().logger


class TableListener(CTableListener):
    """
    The interface provides method signatures to process notifications
    about trading tables events: adding/updating/deleting of rows,
    and changes in a table status.

    """
    def __init__(self, response_listener):
        super().__init__()
        self._refcount = Counter(1)
        self._response_listener = response_listener
        self._response_listener.addRef()
        self._order_monitor = OrderMonitor()
        self._event = EventFD()
        self._init_setup()

    def __del__(self):
        if self._response_listener:
            self._response_listener.release()
        if self._order_monitor:
            del self._order_monitor

    def _init_setup(self):
        """
        Add existing orders, trades and closed trades on system start up
        
        TODO: Need to improve this to mimic an order as this is deleted
        from the orders table when the trade is excuted.
        Currently the trade is pass through.
        """
        log.debug("")
        bom = self._order_monitor
        
        for row in self._response_listener._init['trades']:
            trade_id = row.getTradeID()
            bom._on_order_added(row)
            bom.get_monitors()[trade_id]._state = "OrderExecuted"
            bom.get_monitors()[trade_id]._result = "Executed"
            bom.get_monitors()[trade_id]._total_amount = row.getAmount()
            bom.get_monitors()[trade_id]._trades.append(row)
            row.release()

        for row in self._response_listener._init['orders']:
            trade_id = row.getTradeID()
            if trade_id in bom.get_monitors():
                bom.get_monitors()[trade_id]._on_attach_to_order(row)
            else:
                bom._on_order_added(row)
            row.release()
            
        for row in self._response_listener._init['closed_trades']:
            trade_id = row.getTradeID()
            if trade_id in bom.get_monitors():
                bom.get_monitors()[trade_id]._closed_trades.append(row)
            else:
                bom._on_order_added(row)
                bom.get_monitors()[trade_id]._state = "OrderCanceled"
                bom.get_monitors()[trade_id]._result = "Executed"
            row.release() 
            
    # C++ CallBack
    def addRef(self):
        self._refcount.increment()
        ref = self._refcount.value
        return ref

    # C++ CallBack
    def release(self):
        self._refcount.decrement()
        ref = self._refcount.value
        if self._refcount.value == 0:
            del self
        return ref
        
    # C++ CallBack
    def _on_added(self, rowID, row):
        table_type = row.getTableType()
        log.debug(table_type)
        if table_type == Orders:
            row.__class__ = IO2GOrderRow
            log.info("TradeID :{}, OrderID :{}, Type :{}, Rate :{}, Amount :{}, TimeInForce {}".format(
                row.getTradeID(),
                row.getOrderID(),
                row.getType(),
                row.getRate(),
                row.getAmount(),
                row.getTimeInForce()
                )
            )
            self._order_monitor._on_order_added(row)

        elif table_type == Trades:
            row.__class__ = IO2GTradeRow
            log.info("TradeID :{}, OrderID :{}, Rate {}, Amount :{}".format(
                row.getTradeID(),
                row.getOpenOrderID(),
                row.getOpenRate(),
                row.getAmount()
                )
            )
            self._order_monitor._on_trade_added(row)
            trade_id = row.getTradeID()
            if self._order_monitor.is_executed(trade_id):
                self._send_result(trade_id)
                self._response_listener.stop_waiting()

        elif table_type == ClosedTrades:
            row.__class__ = IO2GClosedTradeRow
            log.info("TradeID :{}, OrderID :{}, Rate {}, Amount :{}".format(
                row.getTradeID(),
                row.getCloseOrderID(),
                row.getCloseRate(),
                row.getAmount()
                )
            )
            self._order_monitor._on_closed_trade_added(row)
            trade_id = row.getTradeID()
            if self._order_monitor.is_executed(trade_id):
                self._send_result(trade_id)
                self._response_listener.stop_waiting()

        elif table_type == Messages:
            row.__class__ = IO2GMessageRow
            text = row.getText()
            log.info(text)
            execution_check = False
            for monitor in self._order_monitor.get_monitors().values():
                trade_id = monitor.order.getTradeID()
                order_ids = monitor.get_order_ids()
                for order_id in order_ids:
                    if order_id in text:
                        self._order_monitor._on_message_added(trade_id, row)
                        execution_check = True
                        break
            if execution_check:
                if self._order_monitor.is_executed(trade_id):
                    self._send_result(trade_id)
                    self._response_listener.stop_waiting()
                
    # C++ CallBack
    def _on_changed(self, rowID, row):
        table_type = row.getTableType()
        log.debug(table_type)
        if row.getTableType() == Accounts:
            row.__class__ = IO2GAccountTableRow
            log.debug("AccountID :{}, Balance :{}, Equity :{}".format(
                row.getAccountID(),
                row.getBalance(),
                row.getEquity()
                )
            )
        elif table_type == Orders:
            row.__class__ = IO2GOrderRow
        
        # elif blaa blaa etc ..
    
    # C++ CallBack
    def _on_deleted(self, rowID, row):
        table_type = row.getTableType()
        log.debug(table_type)
        if table_type == Orders:
            row.__class__ = IO2GOrderRow
            trade_id = row.getTradeID()
            log.info("The order has been deleted. OrderID {}".format(row.getOrderID()))
            self._order_monitor._on_order_deleted(row)
            if self._order_monitor.is_executed(trade_id):
                self._send_result(trade_id)
                self._response_listener.stop_waiting()
                
                
        elif row.getTableType() == Trades:
            row.__class__ = IO2GTradeRow
            log.info("TradeID :{}, OrderID :{}, Rate {}, Amount :{}".format(
                row.getTradeID(),
                row.getOpenOrderID(),
                row.getOpenRate(),
                row.getAmount()
                )
            )

    # C++ CallBack
    def _on_status_changed(self, status):
        log.debug("")
        pass

    def _send_result(self, trade_id):
        """
        For an example the result is printed, but this could be placed into
        a Queue which feeds into a trading system.
        """
        log.debug("")
        print_order_monitor(self._order_monitor.get_monitors()[trade_id])

    def subscribe_events(self, manager):
        """
        Subscribes this class to receive updates.
        """
        manager.addRef()
        accounts_table = manager.getTable(O2GTable.Accounts)
        accounts_table.__class__ = IO2GAccountsTable
        orders_table = manager.getTable(O2GTable.Orders)
        orders_table.__class__ = IO2GOrdersTable
        trades_table = manager.getTable(O2GTable.Trades)
        trades_table.__class__ = IO2GTradesTable
        messages_table = manager.getTable(O2GTable.Messages)
        messages_table.__class__ = IO2GMessagesTable
        closed_trades_table = manager.getTable(O2GTable.ClosedTrades)
        closed_trades_table.__class__ = IO2GClosedTradesTable
        
        #accounts_table.subscribeUpdate(O2GTableUpdateType.Update, self)
        orders_table.subscribeUpdate(O2GTableUpdateType.Insert, self)
        orders_table.subscribeUpdate(O2GTableUpdateType.Update, self)
        orders_table.subscribeUpdate(O2GTableUpdateType.Delete, self)
        trades_table.subscribeUpdate(O2GTableUpdateType.Insert, self)
        #trades_table.subscribeUpdate(O2GTableUpdateType.Update, self)
        trades_table.subscribeUpdate(O2GTableUpdateType.Delete, self)
        closed_trades_table.subscribeUpdate(O2GTableUpdateType.Insert, self)
        closed_trades_table.subscribeUpdate(O2GTableUpdateType.Update, self)
        closed_trades_table.subscribeUpdate(O2GTableUpdateType.Delete, self)
        messages_table.subscribeUpdate(O2GTableUpdateType.Insert, self)

    def unsubscribe_events(self, manager):
        """
        Unsubscribes this class from updates.
        """
        manager.addRef()
        accounts_table = manager.getTable(O2GTable.Accounts)
        accounts_table.__class__ = IO2GAccountsTable
        orders_table = manager.getTable(O2GTable.Orders)
        orders_table.__class__ = IO2GOrdersTable
        trades_table = manager.getTable(O2GTable.Trades)
        trades_table.__class__ = IO2GTradesTable
        messages_table = manager.getTable(O2GTable.Messages)
        messages_table.__class__ = IO2GMessagesTable
        closed_trades_table = manager.getTable(O2GTable.ClosedTrades)
        closed_trades_table.__class__ = IO2GClosedTradesTable
        
        accounts_table.unsubscribeUpdate(O2GTableUpdateType.Update, self)
        orders_table.unsubscribeUpdate(O2GTableUpdateType.Insert, self)
        orders_table.unsubscribeUpdate(O2GTableUpdateType.Update, self)
        orders_table.unsubscribeUpdate(O2GTableUpdateType.Delete, self)
        trades_table.unsubscribeUpdate(O2GTableUpdateType.Insert, self)
        trades_table.unsubscribeUpdate(O2GTableUpdateType.Update, self)
        closed_trades_table.unsubscribeUpdate(O2GTableUpdateType.Insert, self)
        messages_table.unsubscribeUpdate(O2GTableUpdateType.Insert, self)
