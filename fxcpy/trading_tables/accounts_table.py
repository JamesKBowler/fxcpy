from forexconnect import (
    IO2GAccountRow,
    IO2GAccountsTable,
    O2GTable
)


class AccountsTable(object):
    def __init__(self, table_manager):
        self._table_manager = table_manager
        self._set_table()
    
    def _set_table(self):        
        self._table = self._table_manager.getTable(O2GTable.Accounts)
        self._table.__class__ = IO2GAccountsTable
        
    def get_row(self):
        row = self._table.getRow(0)
        if row:
            row.__class__ = IO2GAccountRow
            row.release()
            return row
        
    def get_account_id(self):
        """
        The unique identification number of an account. The number is unique 
        within the database where the account is stored. 
        For example, MINIDEMO or U100D1. The uniqueness of the account itself
        is assured by the combination of the database ID and the value of this
        field.	
        
        Note: In the field labeled "Account", the FX Trading Station displays 
        the value of the AccountName field (for example, 00286255). This 
        value is not equal to the value of the AccountID field (for example 
        286255). Therefore, do not use the AccountName field when the actual 
        AccountID field is required!	

        Returns: string

        """
        row = self.get_row()
        if row:
            return row.getAccountID()
    
    def get_account_name(self):
        """
        The unique name of the account as it is displayed in the FX Trading 
        Station. The name is unique within the database where the account is 
        stored. For example, MINIDEMO or U100D1. The uniqueness of the 
        account itself is assured by the combination of the database ID and 
        the value of this field.	

        Returns: string

        """
        row = self.get_row()
        if row:
            return row.getAccountName()

    def get_balance(self):
        """
        The amount of funds on the account. This amount does not include 
        floating profit and loss. It is expressed in the account currency.	

        Returns: double

        """
        row = self.get_row()
        if row:
            return row.getBalance()

    def get_non_trade_equity(self):
        """
        The amount of accounting transactions that is applied to the account 
        during the current trading day. In other words, this amount is a 
        part of the equity balance that reflects non-trading activity. It 
        is expressed in the account currency and used for calculation of 
        DayPL. The accounting transactions are: deposit, withdrawal and 
        funds transfer. A trading day is from 17:00 through 17:00 Eastern 
        Time (UTC-5). If there are no accounting transactions during the 
        current trading day, the value of this field is 0.0.	

        Returns: double

        """
        row = self.get_row()
        if row:
            return row.getNonTradeEquity()

    def get_m2m_equity(self):
        """
        The equity balance of the account at the beginning of a trading day. 
        It is expressed in the account currency and used for calculation of 
        DayPL. A trading day is from 17:00 through 17:00 Eastern Time (UTC-5).	

        Returns: double

        """
        row = self.get_row()
        if row:
            return row.getM2MEquity()

    def get_used_margin(self):
        """
        The amount of funds used to maintain all open positions on the account. 
        It is expressed in the account currency. If there are no open positions 
        on the account, the value of this field is 0.0.	

        Returns: double

        """
        row = self.get_row()
        if row:
            return row.getUsedMargin()

    def get_used_margin3(self):
        """
        The amount of funds used to maintain all open positions on the account
        with the three-level margin policy. It is expressed in the account 
        currency.
        If there are no open positions on the account, the value of this 
        field is 0.0.	

        Returns: double

        """
        row = self.get_row()
        if row:
            return row.getUsedMargin3()

    def get_account_kind(self):
        """
        The type of the account. 
        
        The possible values are:	
        32	Self-traded account, funds manager account (only LAMM), managed 
            account (only LAMM).
        36	Funds manager account (only PAMM).
        38	Managed account (only PAMM).

        Returns: string

        """
        row = self.get_row()
        if row:
            return row.getAccountKind()

    def get_margin_call_flag(self):
        """
        The limitation state of the account. Each state defines the operations
        that can be performed on the account. 
        
        The possible values are:	
        Y	Margin call (all positions are liquidated, new positions cannot 
            be opened).
        W	Warning of a possible margin call (positions may be closed, new 
            positions cannot be opened).
        Q	Equity stop (all positions are liquidated, new positions cannot 
            be opened up to the end of the trading day).
        A	Equity alert (positions may be closed, new positions cannot be 
            opened up to the end of the trading day).
        N	No limitations (no limitations are imposed on the account 
            operations).

        Returns: string

        """
        row = self.get_row()
        if row:
            return row.getMarginCallFlag()

    def get_last_margin_call_date(self):
        """
        The date and time of the last occurrence of a Margin Call. If the 
        account has never been in the Margin call limitation state, the 
        value of this field is null.	

        Returns: date
        
        """
        row = self.get_row()
        if row:
            return row.getLastMarginCallDate()

    def get_maintenance_type(self):
        """
        The type of the position maintenance. It defines how trade operations
        can be performed on the account. 
        
        The possible values are:	
        Y	Hedging is allowed. In other words, both buy and sell positions 
            can be opened for the same instrument at the same time. To close each 
            buy or sell position, an individual order is required.
        N	Hedging is not allowed. In other words, either a buy or a sell 
            position can be opened for the same instrument at a time. Opening a 
            position for the instrument that already has open position(s) of the 
            opposite trade operation always causes closing or partial closing of 
            the open position(s).
        0	Netting only. In other words, for each instrument there exists 
            only one open position. The amount of the position is the total 
            amount of the instrument, either bought or sold, that has not yet 
            been offset by opposite trade operations.
        D	Day netting. In other words, for each instrument there exists 
            only one open position. Same as Netting only, but within a trading 
            day. If the position is not offset during the same trading day it is 
            opened, it is closed automatically on simulated delivery date (see 
            ValueDate field in the Offers table).
        F	FIFO. Positions open and close in accordance with the FIFO 
            (First-in, First-out) rule. Hedging is not allowed.

        Returns: string

        """
        row = self.get_row()
        if row:
            return row.getMaintenanceType()

    def get_amount_limit(self):
        """
        The maximum amount of an order that is allowed on the account. 
        It is expressed in the base currency of the instrument. 
        For example, if the value is 30000, the maximum amount of an 
        order for EUR/USD is 30,000 Euro, for USD/JPY - 30,000 U.S. dollars, 
        and so on. If there are no restrictions on the maximum amount of 
        an order, the value of this field is 0.	

        Returns: integer

        """
        row = self.get_row()
        if row:
            return row.getAmountLimit()

    def get_base_unit_size(self):
        """
        The size of one lot. In other words, the minimum amount of a 
        position that is allowed on the account. It is expressed in the 
        base currency of the instrument. For example, if the value is 1000, 
        one lot for EUR/USD is 1,000 Euro, for USD/JPY - 1,000 U.S. dollars, 
        and so on. The total amount of a position must be a whole number of 
        lots. It is applicable only for FX instruments. This field is used 
        for information purposes only. The value for all instruments must 
        be obtained from getBaseUnitSize method of the 
        TradingSettingsProvider object.	

        Returns: integer

        """
        row = self.get_row()
        if row:
            return row.getBaseUnitSize()

    def get_maintenance_flag(self):
        """
        The rollover maintenance flag. It defines whether the account is 
        under a rollover maintenance or not. 
        The possible values are:	
        TRUE	The account is under a rollover maintenance.
        FALSE	The account is not under a rollover maintenance.
            
        It is applicable only for funds manager accounts (see AccountKind 
        field above). For all other account types, the value of this field 
        is false.	

        Returns: boolean

        """
        row = self.get_row()
        if row:
            return row.getMaintenanceFlag()

    def get_manager_account_id(self):
        """
        The unique identification number of the funds manager account. 
        The number is unique within the database where the account is 
        stored. For example, MINIDEMO or U100D1. The uniqueness of the 
        funds manager account itself is assured by the combination of the 
        database ID and the value of this field.	
	
        It is applicable only for managed accounts. For all other account 
        types, the value of this field is blank.	

        Returns: string

        """
        row = self.get_row()
        if row:
            return row.getManagerAccountID()

    def get_leverage_profile_id(self):
        """
        The unique identification number of the account leverage profile 
        which defines the margin requirements.	
        Returns: string

        """
        row = self.get_row()
        if row:
            return row.getLeverageProfileID()

    def get_day_pl(self):
        """
        The amount of profits and losses (both floating and realized) of 
        the current trading day. It is expressed in the account currency. 
        A trading day is from 17:00 through 17:00 Eastern Time (UTC-5).	
        
        Note: It is a calculated field and is available only through the 
        Table Manager.	

        Returns: double

        """
        row = self.get_row()
        if row:
            return row.getDayPL()

    def get_equity(self):
        """
        The amount of funds on the account, including profits and losses 
        of all open positions (the floating balance of the account). It is 
        expressed in the account currency.	
        
        Note: It is a calculated field and is available only through the 
        Table Manager.	

 
        Returns: double

        """
        row = self.get_row()
        if row:
            return row.getEquity()
    
    def get_gross_pl(self):
        """
        The amount of profits and losses of all open positions on the 
        account.
        It is expressed in the account currency. The GrossPL equals the 
        difference between the Equity and the Balance of the account.	
        
        Note: It is a calculated field and is available only through the 
        Table Manager.	

        Returns: double

        """
        row = self.get_row()
        if row:
            return row.getGrossPL()

    def get_usable_margin(self):
        """
        The amount of funds available to open new positions or to absorb 
        losses of the existing positions. It is expressed in the account 
        currency. Once the UsableMargin reaches zero, the margin call order 
        is triggered for the account and the positions are automatically 
        liquidated at the best available price. Added together, the
        UsableMargin and UsedMargin make up the Equity of the account.	
        
        Note: It is a calculated field and is available only through the 
        Table Manager.	

        Returns: double
        """
        row = self.get_row()
        if row:
            return row.getUsableMargin()

    def get_atp_id(self):
        """
        The unique identification number of the account trading profile 
        which defines the commission requirements.	

        Returns: string

        """
        row = self.get_row()
        if row:
            return row.getATPID()