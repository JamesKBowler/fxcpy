from forexconnect import (
    IO2GTradeRow,
    IO2GTradesTable,
    O2GTable
)

class TradesTable(object):
    def __init__(self, table_manager):
        self._table_manager = table_manager
        self._set_table()
    
    def _set_table(self):
        """
        Initial table selection.
        """
        self._table = self._table_manager.getTable(O2GTable.Trades)
        self._table.__class__ = IO2GTradesTable
        
    def _find_row(self, trade_id):
        """
        Handle table requests for findRow
        """
        row = self._table.findRow(trade_id)
        if row:
            row.__class__ = IO2GTradeRow
            row.release()
            return row
        
    def get_trade_ids(self):
        """
        A distinctive identification of the open position. The number 
        is exclusive among the same databse that stores the account the 
        position is opened on.
        
        For instance, MINIDEMO or U100D1. the distinctiveness of the open position
        itself is assured by the mixture of the information ID and therefore
        the price of this field.	

        Returns: string

        """
        trades_dict = {}
        for i in range(self._table.size()):
            trade_row = self._table.getRow(i)
            if trade_row:
                trade_row.__class__ = IO2GTradeRow
                trades_dict[trade_row.getTradeID()] = trade_row.getOfferID()
                trade_row.release()
        return trades_dict
    
    def get_account_id(self, trade_id):
        """
        A distinctive identification of the account. The number 
        is exclusive among the same databse that stores the account the 
        position is opened on.
        
        For instance, MINIDEMO or U100D1. the distinctiveness of the account
        itself is assured by the mixture of the information ID and therefore
        the price of this field.

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getAccountID()

    def get_account_name(self, trade_id):
        """
        The unique name of the account the position is opened on. 
        The name is unique within the database where the account is stored. 
        
        For instance, MINIDEMO or U100D1. the distinctiveness of the account
        itself is assured by the mixture of the information ID and therefore
        the price of this field.

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getAccountName()

    def get_account_kind(self, trade_id):
        """
        The type of the account the position is opened on.
        
        The possible values are:
        
        32	Self-traded account, funds manager account (only LAMM), 
                managed account (only LAMM).
        36	Funds manager account (only PAMM).
        38	Managed account (only PAMM).

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getAccountKind()

    def get_offer_id(self, trade_id):
        """
        The unique identification number of the instrument traded.	

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getOfferID()

    def get_amount(self, trade_id):
        """
        The amount of the position. In the case of FX instruments,
        the amount is expressed in the base currency of the instrument. 
        
        In the case of CFD instruments, the amount is expressed in contracts.	

        Returns: integer

        """
        row = self._find_row(trade_id)
        if row:
            return row.getAmount()

    def get_buysell(self, trade_id):
        """
        The trade operation the position is opened by. 
        
        The possible values are:	
        B	Buy.
        S	Sell.

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getBuySell()

    def get_open_rate(self, trade_id):
        """
        The price the position is opened at. 
        
        In the case of FX instruments, it is expressed in the instrument 
        counter currency per one unit  of base currency. In the case of CFD
        instruments, it is expressed in the instrument native currency
        per one contract.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getOpenRate()

    def get_open_time(self, trade_id):
        """
        The date and time when the position is opened.	
        The time zone is defined by the system properties 
        
        SERVER_TIME_UTC and BASE_TIME_ZONE.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getOpenTime()

    def get_open_quote_id(self, trade_id):
        """
        The unique identifier of the pair of prices (bid and ask) 
        the position is opened at.	

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getOpenQuoteID()

    def get_open_order_id(self, trade_id):
        """
        The unique identification number of the order the position 
        is opened by.
        
        The number is unique within the same database that stores the account
        the order is placed on. 
        
        For instance, MINIDEMO or U100D1. the distinctiveness of the order
        itself is assured by the mixture of the information ID and therefore
        the price of this field.

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getOpenOrderID()

    def get_open_order_req_id(self, trade_id):
        """
        The identifier of the order request the position is opened by 
        (see RequestID column in the Orders table).	

        Returns: string
        """
        row = self._find_row(trade_id)
        if row:
            return row.getOpenOrderReqID()

    def get_open_order_request_txt(self, trade_id):
        """
        The custom identifier of the order the position is opened by 
        (see RequestTXT column in the Orders table).	

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getOpenOrderRequestTXT()

    def get_commission(self, trade_id):
        """
        The amount of funds subtracted from the account balance to 
        pay for the broker's service in accordance with the terms and 
        conditions of the account trading agreement. 
        
        It is expressed in the account currency. If commision is not charged
        or has not been charged yet, the value of this field is 0.0.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getCommission()

    def get_rollover_interest(self, trade_id):
        """
        The cumulative amount of funds that is added the account balance 
        for holding the position overnight. 
        
        It is expressed in the account currency.
        
        The value of this field can be positive or negative. 
        
        If the position has not been held overnight, the value of this 
        field is 0.0.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getRolloverInterest()

    def get_tradeid_origin(self, trade_id):
        """
        The unique identification number of the position, the partial 
        closing of which results in the opening of the current position. 
        Otherwise, this field is empty.	

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getTradeIDOrigin()

    def get_used_margin(self, trade_id):
        """
        The amount of funds currently committed to maintain the position. 
        
        It is expressed in the account currency.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getUsedMargin()

    def get_value_date(self, trade_id):
        """
        The simulated delivery date. The date when the position could be 
        automatically closed. The date is provided in the yyyyMMdd format. 
        
        It is applicable only for positions opened on accounts with the day 
        netting trading mode (see MaintenanceType field in the 
        Accounts table). 
        
        Otherwise, the value of this field is blank.	

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getValueDate()

    def get_parties(self, trade_id):
        """
        The unique identifier of the environment that is used to open the 
        position. The identifier is generated by ForexConnect.	

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getParties()

    def get_close(self, trade_id):
        """
        The price at which the position can be closed at the moment. In the 
        case of FX instruments, it is expressed in the instrument counter 
        currency per one unit of base currency. In the case of CFD instruments, 
        it is expressed in the instrument native currency per one contract.
        
        Note: It is a calculated field and is available only through the 
        Table Manager.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getClose()

    def get_gross_pl(self, trade_id):
        """
        The current profit/loss of the position. It is expressed in the 
        account currency.
        
        Note: It is a calculated field and is available only through the 
        Table Manager.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getGrossPL()

    def get_limit(self, trade_id):
        """
        The price of the associated limit order (profit limit level). In
        the case of FX instruments, it is expressed in the instrument
        counter currency per one unit of base currency.
        
        In the case of CFD instruments, it is expressed in the instrument
        native currency per one contract. 
        
        If there is no associated limit order, the value of this field is 0.0.	
        
        Note: It is a calculated field and is available only through the 
        Table Manager. 
        
        It is not applicable for the U.S. based accounts. 
        
        In the case of the accounts subject to the FIFO rule, the value 
        of this field is 0.0.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getLimit()

    def get_pl(self, trade_id):
        """
        The current profit/loss per one lot of the position. It is expressed 
        in the account currency.
        The size of one lot is obtained by getBaseUnitSize method of the 
        TradingSettingsProvider object.	
        
        Note: It is a calculated field and is available only through 
        the Table Manager.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getPL()

    def get_stop(self, trade_id):
        """
        The price of the associated stop order (loss limit level). In the 
        case of FX instruments, it is expressed in the instrument counter 
        currency per one unit of base currency. 
        
        In the case of CFD instruments, it is expressed in the instrument
        native currency per one contract. 
        
        If there is no associated stop order, the value of this field is 0.0.	
        
        Note: It is a calculated field and is available only through the 
        Table Manager.
        
        It is not applicable for the U.S. based accounts. In the case of the 
        accounts subject to the FIFO rule, the value of this field is 0.0.	

        Returns: double
        
        """
        row = self._find_row(trade_id)
        if row:
            return row.getStop()