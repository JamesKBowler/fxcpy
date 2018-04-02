from forexconnect import (
    IO2GClosedTradeRow,
    IO2GClosedTradesTable,
    O2GTable
)


class ClosedTradesTable(object):
    def __init__(self, table_manager):
        self._table_manager = table_manager
        self._set_table()
    
    def _set_table(self):        
        self._table = self._table_manager.getTable(O2GTable.ClosedTrades)
        self._table.__class__ = IO2GClosedTradesTable
        
    def _find_row(self, trade_id):
        row = self._table.findRow(trade_id)
        if row:
            row.__class__ = IO2GClosedTradeRow
            row.release()
            return row
        
    def get_trade_ids(self):
        """
        The unique identification number of the position.
        The number is unique within the same database that stores
        the position account. For example, MINIDEMO or U100D1.
        The uniqueness of the position itself is assured by the
        combination of the database ID and the value of this field.
        It corresponds to the TradeID field in the Trades table.

        Returns: string

        """
        closed_trades_dict = {}
        for i in range(self._table.size()):
            row = self._table.getRow(i)
            if row:
                row.__class__ = IO2GClosedTradeRow
                closed_trades_dict[row.getTradeID()] = row.getInstrument()
                row.release()
        return closed_trades_dict
    
    def get_account_id(self, trade_id):
        """
        The unique identification number of the position account.
        The number is unique within the database where the account
        is stored. For example, MINIDEMO or U100D1. The uniqueness
        of the account itself is assured by the combination of the
        database ID and the value of this field.

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getAccountID()

    def get_account_name(self, trade_id):
        """
        The unique name of the position account. The name is unique
        within the database where the account is stored.
        For example, MINIDEMO or U100D1. The uniqueness of the
        account itself is assured by the combination of the database
        ID and the value of this field. It is the name that the
        FX Trading Station displays to its user.

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getAccountName()
        
    def get_account_kind(self, trade_id):
        """
        The type of the position account.
        
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
        The amount of the closed position. In the case of FX instruments,
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

    def get_gross_pl(self, trade_id):
        """
        The profit/loss of the position. It is expressed in the account currency.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getGrossPL()

    def get_commission(self, trade_id):
        """
        The amount of funds subtracted from the account balance to pay for the 
        broker's service in accordance with the terms and conditions of the 
        account trading agreement. It is expressed in the account currency. 
        If commission has not been charged, the value of this field is 0.0.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getCommission()

    def get_rollover_interest(self, trade_id):
        """
        The cumulative amount of funds added to the account balance for 
        holding the position overnight. It is expressed in the account 
        currency. The value of this field can be positive or negative. 
        If the position has not been held overnight, the value of this 
        field is 0.0.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getRolloverInterest()

    def get_open_rate(self, trade_id):
        """
        The price the position is opened at. In the case of FX instruments, 
        it is expressed in the instrument counter currency per one unit of 
        base currency. In the case of CFD instruments, it is expressed in t
        he instrument native currency per one contract.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getOpenRate()

    def get_openquote_id(self, trade_id):
        """
        The unique identifier of the pair of prices (bid and ask) the 
        position is opened at.	

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getOpenQuoteID()

    def get_open_time(self, trade_id):
        """
        The date and time when the position is opened.
        The time zone is defined by the system properties
        SERVER_TIME_UTC and BASE_TIME_ZONE.	

        Returns: date

        """
        row = self._find_row(trade_id)
        if row:
            return row.getOpenTime()

    def get_open_order_id(self, trade_id):
        """
        The unique identification number of the order the position is 
        opened by. The number is unique within the same database that
        stores the account the order is placed on. For example, 
        MINIDEMO or U100D1. The uniqueness of the order itself is assured 
        by the combination of the database ID and the value of this field.	

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getOpenOrderID()

    def get_open_order_req_id(self, trade_id):
        """
        The unique identifier of the order request the position is 
        opened by (see RequestID column in the Orders table).	

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

    def get_open_order_parties(self, trade_id):
        """
        The unique identifier of the environment that is used to open 
        the position. The identifier is generated by ForexConnect.	

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getOpenOrderParties()

    def get_close_rate(self, trade_id):
        """
        The price the position is closed at. In the case of FX 
        instruments, it is expressed in the instrument counter currency 
        per one unit of base currency. In the case of CFD instruments, 
        it is expressed in the instrument native currency per one contract.	

        Returns: double

        """
        row = self._find_row(trade_id)
        if row:
            return row.getCloseRate()

    def get_close_quote_id(self, trade_id):
        """
        The unique identifier of the pair of prices (bid and ask) 
        the position is closed at.	

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getCloseQuoteID()

    def get_close_time(self, trade_id):
        """
        The date and time when the position is closed.	
        The time zone is defined by the system properties
        SERVER_TIME_UTC and BASE_TIME_ZONE.	

        Returns: date

        """
        row = self._find_row(trade_id)
        if row:
            return row.getCloseTime()

    def get_close_order_id(self, trade_id):
        """
        The unique identification number of the order the position 
        is closed by. The number is unique within the same database 
        that stores the account the order is placed on. For example, 
        MINIDEMO or U100D1. The uniqueness of the order itself is 
        assured by the combination of the database ID and the 
        value of this field.	

        Returns: string

        """
        row = self._find_row(trade_id)
        if row:
            return row.getCloseOrderID()

    def get_close_order_req_id(self, trade_id):
        """
        The unique identifier of the order request the position is 
        closed by (see RequestID column in the Orders table).	

        Returns: string
        
        """
        row = self._find_row(trade_id)
        if row:
            return row.getCloseOrderReqID()

    def get_close_order_request_txt(self, trade_id):
        """
        The custom identifier of the order the position is closed by 
        (see RequestTXT column in the Orders table).	

        Returns: string
        
        """
        row = self._find_row(trade_id)
        if row:
            return row.getCloseOrderRequestTXT()

    def get_close_order_parties(self, trade_id):
        """
        The unique identifier of the environment that is used to 
        close the position. The identifier is generated by ForexConnect.	

        Returns: string
        
        """
        row = self._find_row(trade_id)
        if row:
            return row.getCloseOrderParties()

    def get_trade_id_origin(self, trade_id):
        """
        The unique identification number of the position, the 
        partial closing of which results in the opening of the 
        current position. Otherwise, the value of this field 
        is blank.	

        Returns: string
        
        """
        row = self._find_row(trade_id)
        if row:
            return row.getTradeIDOrigin()

    def get_trade_id_remain(self, trade_id):
        """
        The unique identification number of the position opened 
        as the result of the current position partial closing. 
        Otherwise, the value of this field is blank.	

        Returns: string
        
        """
        row = self._find_row(trade_id)
        if row:
            return row.getTradeIDRemain()

    def get_value_date(self, trade_id):
        """
        The simulated delivery date. The date when the position 
        could have been automatically closed. It is provided in 
        the yyyyMMdd format.	
        This field is applicable for positions opened on accounts
        with the day netting trading mode (see MaintenanceTypefield 
        n the Accounts table).	

        Returns: string
        
        """
        row = self._find_row(trade_id)
        if row:
            return row.getValueDate()