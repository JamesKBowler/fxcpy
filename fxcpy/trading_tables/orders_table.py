from forexconnect import (
    IO2GOrderRow,
    IO2GOrdersTable,
    O2GTable
)


class OrdersTable(object):
    def __init__(self, table_manager):
        self._table_manager = table_manager
        self._set_table()
    
    def _set_table(self):        
        self._table = self._table_manager.getTable(O2GTable.Orders)
        self._table.__class__ = IO2GOrdersTable
        
    def _find_row(self, order_id):
        row = self._table.findRow(order_id)
        if row:
            row.__class__ = IO2GOrderRow
            row.release()
            return row

    def get_order_ids(self):
        """
        The unique identification number of the order. The number is unique 
        within the same database that stores the account the order is placed 
        on. For example, MINIDEMO or U100D1. The uniqueness of the order 
        itself is assured by the combination of the database ID and the value 
        of this field.

        Returns: string

        """
        orders_dict = {}
        for i in range(self._table.size()):
            row = self._table.getRow(i)
            if row:
                row.__class__ = IO2GOrderRow
                orders_dict[row.getOrderID()] = row.getInstrument()
                row.release()
        return orders_dict

    def get_order_id(self):
        """
        The unique identification number of the order. The number is unique 
        within the same database that stores the account the order is placed 
        on. For example, MINIDEMO or U100D1. The uniqueness of the order 
        itself is assured by the combination of the database ID and the value 
        of this field.

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getOrderID()

    def get_request_id(self):
        """
        The identifier of the request to create an order. One request can 
        create several orders. For example, if an entry order is created 
        with stop and limit orders attached, the table contains several 
        orders with the same RequestID.
        If after its creation the order is changed, then this field represents
        the unique identifier of the request to make the last change.
        
        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getRequestID()

    def get_rate(self):
        """
        The price the order is placed at. In the case of FX instruments, it is
        expressed in the instrument counter currency per one unit of base 
        currency. In the case of CFD instruments, it is expressed in the 
        instrument native currency per one contract.	
        In the case of open/close market orders and pegged stop/limit orders, 
        the value of this field is 0.0.
        
        Returns: double

        """
        row = self._find_row(order_id)
        if row:
            return row.getRate()

    def get_execution_rate(self):
        """
        The price the order is executed at. In the case of FX instruments, 
        it is expressed in the instrument counter currency per one unit of 
        base currency. In the case of CFD instruments, it is expressed in 
        the instrument native currency per one contract. Applicable only 
        when the order is filled completely or partially. In other words, 
        this field has a meaningful value if the order status is either 
        Pending Calculated, Executing or Executed. For details, please refer 
        to Orders State Machinessection. If the order is in any other state, 
        the value of this field is 0.0. If the order is filled in several 
        steps, the value of this field may differ for every partiall fill.	

        Returns: double

        """
        row = self._find_row(order_id)
        if row:
            return row.getExecutionRate()

    def get_rate_min(self):
        """
        The minimum price at which the order can be filled. In the case of 
        FX instruments, it is expressed in the instrument counter currency 
        per one unit of base currency. In the case of CFD instruments, it 
        is expressed in the instrument native currency per one contract. 
        It is applicable only for open/close range orders. For all other 
        order types, the value of this field is 0.0.	

        Returns: double

        """
        row = self._find_row(order_id)
        if row:
            return row.getRateMin()

    def get_rate_max(self):
        """
        The maximum price at which the order can be filled. In the case of 
        FX instruments, it is expressed in the instrument counter currency 
        per one unit of base currency. In the case of CFD instruments, it 
        is expressed in the instrument native currency per one contract. 
        
        It is applicable only for open/close range orders. 
        
        For all other order types, the value of this field is 0.0.	

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getRateMax()

    def get_trade_id(self):
        """
        The unique identification number of the position to be opened/closed 
        by the order. The number is unique within the same database that 
        stores the account the position can be opened or closed on. For 
        example, MINIDEMO or U100D1. The uniqueness of the position itself 
        is assured by the combination of the database ID and the value of 
        this field.	
        In the case the opening order fills partially, the system opens a 
        position for every partial fill. Every position has unique TradeID. 
        Therefore, after a partial fill, this field has the unique value. 
        Likewise, the value of this field changes if the order closes the 
        particular position and fills partially.	
        In some cases, this number does not reference any particular 
        position. 
        
        Such cases are:	
        The order is placed as the Net Amount order.	
            
        The order is placed to close positions under the following conditions:	
        - the order is placed on the account where hedging is not allowed 
            (see MaintenanceType field in the Accountstable);	
        - the order is placed in the opposite direction (buy or sell) 
            to the positions trade operation.	

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getTradeID()

    def get_account_id(self):
        """
        The unique identification number of the account the order is placed 
        on. The number is unique within the database where the account is 
        stored. For example, MINIDEMO or U100D1. The uniqueness of the 
        account itself is assured by the combination of the database ID 
        and the value of this field.	

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getAccountID()

    def get_account_name(self):
        """
        The unique name of the account the order is placed on. The name is 
        unique within the database where the account is stored. For example, 
        MINIDEMO or U100D1. The uniqueness of the account itself is assured 
        by the combination of the database ID and the value of this field.	

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getAccountName()

    def get_offer_id(self):
        """
        The unique identification number of the instrument the order is 
        placed for.	

        Returns: boolean

        """
        row = self._find_row(order_id)
        if row:
            return row.getOfferID()

    def get_net_quantity(self):
        """
        The Net Amount order flag. It defines whether the order is a Net 
        Amount order or not. The possible values are:	
        TRUE	The order is a Net Amount order.
        FALSE	The order is not a Net Amount order.
        
        The Net Amount order closes all positions of the specified instrument 
        and account that are in the direction (buy or sell) opposite to the 
        direction of the Net Amount order.	
            
        The following types of order can be Net Amount orders:
        SE - entry stop.	
        LE - entry limit.	
        STE - trailing entry stop.	
        LTE - trailing entry limit.	
        CM - close market.	

        Returns: boolean

        """
        row = self._find_row(order_id)
        if row:
            return row.getNetQuantity()

    def get_buy_sell(self):
        """
        The direction of the trade. The possible values are:	
        B	The order is placed to buy an instrument.
        S	The order is placed to sell an instrument.

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getBuySell()

    def get_stage(self):
        """
        The order action. It defines whether the order is placed to open or 
        close a position. The possible values are:	
        O	The order is placed to open a position.
        C	The order is placed to close a position.

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getStage()

    def get_type(self):
        """
        The order type. The possible values are:	
        S	Stop.
        ST	Trailing Stop.
        L	Limit.
        SE	Entry Stop.
        LE	Entry Limit.
        STE	Trailing Entry Stop.
        LTE	Trailing Entry Limit.
        C	Close.
        CM	Close Market.
        CR	Close Range.
        O	Open.
        OM	Open Market.
        OR	Open Range.
        M	Margin Call.

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getType()

    def get_status(self):
        """
        The state of the order. The possible values are:	
        W	Waiting.
        P	In process.
        I	Dealer intervention.
        Q	Requoted.
        U	Pending calculated.
        E	Executing.
        S	Pending Canceled.
        C	Canceled.
        R	Rejected.
        T	Expired.
        F	Executed.

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getStatus()

    def get_amount(self):
        """
        The amount of the order. In the case of FX instruments, the amount is 
        expressed in the base currency of an instrument. In the case of CFD 
        instruments, the amount is expressed in contracts.	
	
        If the order is filled completely at the first attempt or rejected 
        in the whole amount, it is the initial amount of the order.	
        If the order is filled completely in several attempts, it is the amount
        of the last portion to be filled.	
        If the order is filled partially, it is the remaining amount to be filled.	
        If the order is partially rejected, it is the rejected (unfilled) amount.	
        If the entire order is waiting for execution, it is the initial amount 
        of the order.	
            
        Regardless of the order direction (buy or sell), the value of this 
        field is positive.	
        In the case of the If-Then order, the value of this field is 0.	

        Returns: integer

        """
        row = self._find_row(order_id)
        if row:
            return row.getAmount()

    def get_status_time(self):
        """
        The date and time of the last update of the order state.	
        The time zone is defined by the system properties SERVER_TIME_UTC and 
        BASE_TIME_ZONE.	

        Returns: date

        """
        row = self._find_row(order_id)
        if row:
            return row.getStatusTime()

    def get_life_time(self):
        """
        The time, during which the trader must accept or reject the order 
        requoted by the dealer. The time is expressed in seconds. This field 
        is not currently in use.	

        Returns: integer

        """
        row = self._find_row(order_id)
        if row:
            return row.getLifetime()

    def get_at_market(self):
        """
        The distance from the Rate within which the trader allows the order 
        to be executed. It is expressed in pips. If the market price moves 
        beyond the allowed distance, then the order cannot be executed. This 
        field is applicable only for open/close range orders. For all other 
        types of orders, the value of this field is 0.0.	

        Returns: double

        """
        row = self._find_row(order_id)
        if row:
            return row.getAtMarket()

    def get_trail_step(self):
        """
        The number of pips the market should move before the order moves the 
        same number of pips after it.	
        It is applicable only for trailing orders (trailing stop, entry 
        trailing stop/limit). Otherwise, the value of this field is 0.	
        Note: If the trailing order is dynamic (automatically updates every 
        0.1 of a pip), then the value of this field is 1.	

        Returns: integer

        """
        row = self._find_row(order_id)
        if row:
            return row.getTrailStep()

    def get_trail_rate(self):
        """
        The market price at the time the order automatically moves following 
        the market fluctuations. In the case of FX instruments, it is 
        expressed in the instrument counter currency per one unit of base 
        currency. In the case of CFD instruments, it is expressed in the 
        instrument native currency per one contract.	
	
        If the order has not followed the market yet, the value of this 
        field provides the initial market price at the time when the order 
        is placed. It is applicable only for trailing orders (trailing stop, 
        entry trailing stop/limit). Otherwise, the value of this field 
        is 0.0.	

        Returns: double

        """
        row = self._find_row(order_id)
        if row:
            return row.getTrailRate()

    def get_time_inforce(self):
        """
        The time-in-force option of the order. The possible values are:	
        GTC	Good Till Cancelled (Open/Close Market, Entry, Stop, and Limit 
        orders).
        IOC	Immediate Or Cancel (Open/Close Market, Open/Close, and Open/Close 
        Range orders).
        FOK	Fill Or Kill (Open/Close Market, Open/Close, and Open/Close 
        Range orders).
        DAY	Day Order (Open/Close Market, Entry, Stop, and Limit orders).
        GTD	Good Till Date (Open/Close Market, Entry, Stop, and Limit orders).

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getTimeInForce()

    def get_account_kind(self):
        """
        The type of the account the order is placed on. The possible values are:	
        32	Self-traded, funds manager (only LAMM), managed (only LAMM) accounts.
        36	Funds manager account (only PAMM).
        38	Managed account (only PAMM).

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getAccountKind()

    def get_request_txt(self):
        """
        The custom identifier of the order. For example, LimitEntryOrder.	

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getRequestTXT()

    def get_contingent_order_id(self):
        """
        The unique identifier of an existing contingency group which the order
        is linked to. The number is unique within the same database that store
        s the account the contingent order is placed on. 
        For example, MINIDEMO or U100D1. The uniqueness of the order itself is
        assured by the combination of the database ID and the value of this 
        field.	
        It is applicable only for orders included in an OCO order or 
        secondary orders of ELS and OTO orders. Otherwise, the value of this 
        field is blank.	

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getContingentOrderID()

    def get_contingency_type(self):
        """
        The type of the contingent order to which the order is linked. It is 
        applicable only for orders included in an OCO order or secondary 
        orders of ELS, OTO and OTOCO orders. The possible values are:	
        1	OCO order.
        2	OTO order.
        3	ELS order.
        4	OTOCO order.
        
        For all other orders, the value of this field is 0.

        Returns: integer

        """
        row = self._find_row(order_id)
        if row:
            return row.getContingencyType()

    def get_primary_id(self):
        """
        The unique identification number of the primary order of ELS, OTO 
        or OTOCO contingent orders to which the order is linked. The number 
        is unique within the same database that stores the account the 
        primary order is placed on. For example, MINIDEMO or U100D1. The 
        uniqueness of the order itself is assured by the combination of the 
        database ID and the value of this field.	
        It is applicable only for secondary orders of ELS, OTO and OTOCO 
        contingent orders. Otherwise, the value of this field is blank.	

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getPrimaryID()

    def get_origin_amount(self):
        """
        The original amount of the order when it is placed. In the case 
        of FX instruments, the amount is expressed in the base currency 
        of an instrument. In the case of CFD instruments, the amount is 
        expressed in contracts. This field has the same value for the 
        lifetime of the order.	


        Returns: integer

        """
        row = self._find_row(order_id)
        if row:
            return row.getOriginAmount()

    def get_filled_amount(self):
        """
        The amount of the last order portion filled. In the case of 
        FX instruments, the amount is expressed in the base currency 
        of an instrument. In the case of CFD instruments, the amount 
        is expressed in contracts. If the order is rejected or canceled, 
        the value of this field is 0.	

        Returns: integer

        """
        row = self._find_row(order_id)
        if row:
            return row.getFilledAmount()

    def get_working_indicator(self):
        """
        The working indicator flag. It defines whether the order is 
        active on the market or not. The possible values are:	
        Y	The order is active.
        N	The order is inactive.
            
        It is applicable only for secondary orders of ELS, OTO and 
        OTOCO orders. For all other orders, the value of this field is Y.	


        Returns: boolean

        """
        row = self._find_row(order_id)
        if row:
            return row.getWorkingIndicator()

    def get_peg_type(self):
        """
        The price used to calculate the pegged order price. Pegged means 
        that the price is specified as an offset to one of the following 
        prices:	
        O	The stop/limit order is set as a distance in pips to the open 
        price (the pegged stop/limit order).
        M	The stop/limit order is set as a distance in pips to the 
        close price (the pegged stop/limit order).
            
        This field is applicable only for stop/limit orders and secondary 
        orders of ELS orders. For all other order types, the value of 
        this field is blank.	

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getPegType()

    def get_peg_offset(self):
        """
        The offset to the price specified in the PegType field. It is 
        expressed in pips. This field is applicable only for stop/limit 
        orders and secondary orders of ELS orders. For these orders the 
        value of this field can be positive or negative. For all other 
        orders, the value of this field is 0.0.	

        Returns: double

        """
        row = self._find_row(order_id)
        if row:
            return row.getPegOffset()

    def get_expire_date(self):
        """
        The expiration date and time of the order. It is applicable only 
        for the orders with the DAY or GTD time-in-force option.	
        The time zone is defined by the system properties SERVER_TIME_UTC 
        and BASE_TIME_ZONE.	


        Returns: date

        """
        row = self._find_row(order_id)
        if row:
            return row.getExpireDate()

    def get_value_date(self):
        """
        The simulated delivery date. The date when the position could be 
        automatically closed. The position is closed only if the order is 
        executed and opens a position. This field is provided in the 
        yyyyMMdd format. It is applicable for orders placed from accounts 
        with the day netting trading mode (see MaintenanceType field in 
        the Accounts table). Otherwise, the value of this field is blank.	

        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getValueDate()

    def get_parties(self):
        """
        The unique identifier of the environment that is used to place 
        the order. The identifier is generated by ForexConnect.	



        Returns: string

        """
        row = self._find_row(order_id)
        if row:
            return row.getParties()

    def get_limit(self):
        """
        The price of the associated limit order (the profit limit level). 
        In the case of FX instruments, it is expressed in the instrument 
        counter currency per one unit of base currency. In the case of CFD 
        instruments, it is expressed in the instrument native currency per 
        one contract.	
	
        It is applicable only for opening orders (Entry or Market).	
        If there is no associated limit order, the value of this field 
        is 0.0.	
        If the associated limit order is a pegged order, the value of this 
        field is 0.0.	
            
        Note: It is a calculated field and is available only through 
        the Table Manager. It is not applicable for the U.S. accounts. 
        In the case of the accounts subject to the FIFO rule, the value 
        of this field is 0.0.	


        Returns: double

        """
        row = self._find_row(order_id)
        if row:
            return row.getLimit()
            
    def get_stop(self):
        """
        The price of the associated stop order (the loss limit level). In 
        the case of FX instruments, it is expressed in the instrument 
        counter currency per one unit of base currency. In the case of CFD 
        instruments, it is expressed in the instrument native currency per 
        one contract.		
        It is applicable only for opening orders (Entry or Market).	
        If there is no associated stop order, the value of this field is 0.0.	
        If the associated stop order is a pegged order, the value of this 
        field is 0.0.	
            
        Note: It is a calculated field and is available only through the 
        Table Manager. It is not applicable for the U.S. accounts. In the 
        case of the accounts subject to the FIFO rule, the value of this 
        field is 0.0.	


        Returns: double

        """
        row = self._find_row(order_id)
        if row:
            return row.getStop()

    def get_stop_trail_step(self):
        """
        The trailing step of the associated trailing stop order or secondary 
        entry stop order of an ELS order. It is expressed in pips. For 
        details, see TrailStep. It is applicable only for opening orders 
        (Entry or Market). If there is no associated trailing stop order, 
        the value of this field is 0. 	
	
        Note: It is a calculated field and is available only through the 
        Table Manager.	


        Returns: integer

        """
        row = self._find_row(order_id)
        if row:
            return row.getStopTrailStep()

    def get_stop_trail_rate(self):
        """
        The trailing rate of the associated trailing stop order or secondary 
        entry stop order of an ELS order. In the case of FX instruments, it 
        is expressed in the instrument counter currency per one unit of base 
        currency. In the case of CFD instruments, it is expressed in the 
        instrument native currency per one contract. For details, see 
        TrailRate. It is applicable only for opening orders (Entry or Market). 
        If there is no associated trailing stop order, the value of this 
        field is 0.0. 	
	
        Note: It is a calculated field and is available only through the 
        Table Manager.	

        Returns: double
        """
        row = self._find_row(order_id)
        if row:
            return row.getStopTrailRate()