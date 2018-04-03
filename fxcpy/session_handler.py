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
from fxcpy.listeners.session_monitoring import SessionMonitoring
from fxcpy.listeners.response_listener import ResponseListener
from fxcpy.listeners.table_listener import TableListener

from fxcpy.trading.trading_commands import TradingCommands
from fxcpy.trading.trading_settings_provider import TradingSettingsProvider

from fxcpy.factory.price_history import MarketData

from fxcpy.trading_tables.offers_table import OffersTable
from fxcpy.trading_tables.orders_table import OrdersTable
from fxcpy.trading_tables.accounts_table import AccountsTable
from fxcpy.trading_tables.trades_table import TradesTable
from fxcpy.trading_tables.closed_trades_table import ClosedTradesTable
from fxcpy.trading_tables.summary_table import SummaryTable
from fxcpy.trading_tables.messages_table import MessagesTable
    
from fxcpy.exception import LoginFailed

from forexconnect import (
    CO2GTransport,
    Accounts,
    Offers,
    Yes,
    No
)


class SessionHandler(object):
    """
    The SessionHandler class will ensure the correct login
    sequance is carried out for the ForexconnectAPI to
    function correctly and provide access to some of the 
    python implementation.
    
    """
    def __init__(
        self, account, password, url, env,
        load_tables=False
    ):
        self.is_connected = False
        self._session = CO2GTransport.createSession()
        # Monitor session status
        self.session_status = SessionMonitoring(self._session)
        self._session.subscribeSessionStatus(self.session_status)
        self.login(account, password, url, env, load_tables)
        
    def __del__(self):
        """
        Clean up
        """
        if self.is_connected:
            self._session.unsubscribeResponse(self.response_listener)
            self._session.logout()
        self._session.unsubscribeSessionStatus(self.session_status)
        
    def login(self, account, password, url, env, load_tables=False):
        """
        Pre-login setup.
        """
        if not self.is_connected:
            # Option must happen before login
            if load_tables:
                self._session.useTableManager(Yes, None)
            else:
                self._session.useTableManager(No, None)
            # Create live session with fxcm
            self._session.login(account, password, url, env)
            # Block until login completed
            self.is_connected = (
                self.session_status.wait_events() and 
                self.session_status.is_connected()
            )
            if not self.is_connected:
                raise LoginFailed
            # Setup a responce listener
            self.response_listener = ResponseListener(self._session)
            self._session.subscribeResponse(self.response_listener)
            self.response_listener.wait_events()
            # If the table manager has been loaded, then setup a table
            # listener (in memory tables have higher in CPU useage)
            if load_tables: 
                self.table_manager = self._session.getTableManager()
                self._table_listener = TableListener(self.response_listener)
                self._table_listener.subscribe_events(self.table_manager)
                self._offers_table = OffersTable(self.table_manager)
                self._orders_table = OrdersTable(self.table_manager)
                self._accounts_table = AccountsTable(self.table_manager)
                self._trades_table = TradesTable(self.table_manager)
                self._closed_trades_table = ClosedTradesTable(self.table_manager)
                self._messages_table = MessagesTable(self.table_manager)
                self._summary_table = SummaryTable(self.table_manager)
                self.table_manager_loaded = True
            
            self.trading_settings_provider = TradingSettingsProvider(
                self._session.getLoginRules().getTradingSettingsProvider()
            )
            # Get account ID
            lr = self._session.getLoginRules()
            accounts_response = lr.getTableRefreshResponse(Accounts)
            response_factory = self._session.getResponseReaderFactory()
            if response_factory:
                accountsReader = response_factory.createAccountsTableReader(accounts_response)
                account = accountsReader.getRow(0)
                self.account_id = account.getAccountID()
                
            # Trading Commands setup
            offers_response = lr.getTableRefreshResponse(Offers)
            offers_reader = response_factory.createOffersTableReader(offers_response)
            offer_attribs = {}
            tsp = self.trading_settings_provider
            for i in range(offers_reader.size()):
                row = offers_reader.getRow(i)
                instrument = row.getInstrument()
                offer_id = row.getOfferID()
                offer_attribs[offer_id] = tsp.get_base_unit_size(instrument, account)                    
            self._trading_commands = TradingCommands(
                self._session,
                self.account_id,
                offer_attribs
            )
            
            # Market Data
            self._market_data = MarketData(
                self._session,
                self.response_listener,
                self._session.getResponseReaderFactory(),
                self._session.getRequestFactory()
            )

    def logout(self):
        """
        Logout of an existing session with FXCM
        """
        if self.is_connected:
            self._session.logout()
            self.session_status.wait_events()
            self.is_connected = False
            
    def get_market_data(self):
        return self._market_data
    
    def get_offers_table(self):
        """
        Returns OffersTable
        """
        if self.table_manager_loaded:
            return self._offers_table
        else:
            return None
        
    def get_orders_table(self):
        """
        Returns OrdersTable
        """
        if self.table_manager_loaded:
            return self._orders_table
        else:
            return None
        
    def get_accounts_table(self):
        """
        Returns AccountsTable
        """
        if self.table_manager_loaded:
            return self._accounts_table
        else:
            return None
        
    def get_trades_table(self):
        """
        Returns TradesTable
        """
        if self.table_manager_loaded:
            return self._trades_table
        else:
            return None
        
    def get_closed_trades_table(self):
        """
        Returns ClosedTradesTable
        """
        if self.table_manager_loaded:
            return self._closed_trades_table
        else:
            return None
        
    def get_messages_table(self):
        """
        Returns MessagesTable
        """
        if self.table_manager_loaded:
            return self._messages_table
        else:
            return None
        
    def get_summary_table(self):
        """
        Returns SummaryTable
        """
        if self.table_manager_loaded:
            return self._summary_table
        else:
            return None
        
    def get_trading_commands(self):
        """
        Returns TradingCommands
        """
        if self._trading_commands:
            return self._trading_commands
        else:
            return None
        
    def get_table_listener(self):
        """
        Return the TableListner class
        """
        if self.table_manager_loaded:
            return self._table_listener
        else:
            return None
        
    def get_order_monitor(self):
        """
        Return the OrderMonitor
        """
        if self.table_manager_loaded:
            return self._table_listener._order_monitor
        else:
            return None
        
    def get_trade_settings_provider(self):
        """
        Return the TradingSettingProvider
        """
        if self._trade_settings_provider:
            return self._trade_settings_provider
        else:
            return None