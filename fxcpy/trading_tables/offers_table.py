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
from forexconnect import (
    IO2GOfferRow,
    IO2GOffersTable,
    O2GTable
)


class OffersTable(object):
    def __init__(self, table_manager):
        if not table_manager:
            raise AttributeError("Table Manager not loaded")
        self._table_manager = table_manager
        self._set_table()
    
    def _set_table(self):        
        self._table = self._table_manager.getTable(O2GTable.Offers)
        self._table.__class__ = IO2GOffersTable
        
    def _find_row(self, offer_id):
        row = self._table.findRow(offer_id)
        if row:
            row.__class__ = IO2GOfferRow
            row.release()
            return row

    def get_offer_ids(self):
        """
        The unique identification number of the instrument.	

        Returns: dict

        """
        offers_dict = {}
        for i in range(self._table.size()):
            row = self._table.getRow(i)
            if row:
                row.__class__ = IO2GOfferRow
                offers_dict[row.getInstrument()] = row.getOfferID()
                row.release()
        return offers_dict

    def get_instrument(self, offer_id):
        """
        The symbol of the instrument. For example, EUR/USD, USD/JPY, GBP/USD.	

        Returns: string

        """
        row = self._find_row(offer_id)
        if row:
            return row.getInstrument()

    def get_quote_id(self, offer_id):
        """
        The unique identification number of the pair of prices (bid and ask)
        the instrument can be traded at.	

        Returns: string

        """
        row = self._find_row(offer_id)
        if row:
            return row.getQuoteID()

    def get_bid(self, offer_id):
        """
        The current market price the instrument can be sold at. In the case of 
        FX instruments, it is expressed in the instrument counter currency per 
        one unit of base currency. In the case of CFD instruments, it is 
        expressed in the instrument native currency per one contract.	

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getBid()

    def get_ask(self, offer_id):
        """
        The current market price the instrument can be bought at. In the case
        of FX instruments, it is expressed in the instrument counter currency 
        per one unit of base currency. In the case of CFD instruments, it is 
        expressed in the instrument native currency per one contract.	

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getAsk()

    def get_bid_tradable(self, offer_id):
        """
        The usage of the bid price. It defines whether the bid price of the 
        instrument is available for trading or not. The possible values are:	
        T	The bid price is available for trading.
        I	The bid price is view only.
        N	The bid price is not available for trading.

        Returns: string

        """
        row = self._find_row(offer_id)
        if row:
            return row.getBidTradable()

    def get_ask_tradable(self, offer_id):
        """
        The usage of the ask price. It defines whether the ask price of the 
        instrument is available for trading or not. The possible values are:	
        T	The ask price is available for trading.
        I	The ask price is view only.
        N	The ask price is not available for trading.

        Returns: string

        """
        row = self._find_row(offer_id)
        if row:
            return row.getAskTradable()

    def get_high(self, offer_id):
        """
        The highest ask price (buy price) of the instrument for the current 
        trading day. In the case of FX instruments, it is expressed in the 
        instrument counter currency per one unit of base currency. In the case
        of CFD instruments, it is expressed in the instrument native currency 
        per one contract. A trading day is from 17:00 through 17:00 Eastern 
        Time (UTC-5).	

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getHigh()

    def get_low(self, offer_id):
        """
        The lowest bid price (sell price) of the instrument for the current
        trading day. In the case of FX instruments, it is expressed in the 
        instrument counter currency per one unit of base currency. In the
        case of CFD instruments, it is expressed in the instrument native
        currency per one contract. A trading day is from 17:00 through 17:00
        Eastern Time (UTC-5).	

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getLow()

    def get_buy_interest(self, offer_id):
        """
        The interest amount added to the account balance for holding a one 
        lot long (buy) position overnight. In the case of FX instruments, 
        lot size is determined by the system base unit size. In the case of
        CFD instruments, lot size equals to one contract. The interest amount 
        is expressed in the account currency and can be positive or negative.	
            
        Note: If the account base unit size differs from the system base 
        unit size, to get the proper interest amount for the account, 
        
        use the following formula:	
        
        Offer.BuyInterest/SystemProperties.Base_Unit_Size* Account.Base_Unit_Size	
        
        This formula is applicable for FX instruments only.	

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getBuyInterest()

    def get_sell_interest(self, offer_id):
        """
        The interest amount added to the account balance for holding a one lot
        short (sell) position overnight. In the case of FX instruments, lot size
        is determined by the system base unit size. In the case of CFD instruments,
        lot size equals to one contract. The interest amount is expressed in 
        the account currency and can be positive or negative.	
            
        Note: If the account base unit size differs from the system base unit size,
        to get the proper interest amount for the account, 
        
        use the following formula:	
        Offer.SellInterest/SystemProperties.Base_Unit_Size* Account.Base_Unit_Size	
        This formula is applicable for FX instruments only.	

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getSellInterest()

    def get_volume(self, offer_id):
        """
        The tick volume of the current minute. The value of this field represents 
        the number of ticks happened during the current minute.	

        Returns: integer

        """
        row = self._find_row(offer_id)
        if row:
            return row.getVolume()

    def get_contract_currency(self, offer_id):
        """
        The base currency of the instrument (for example, EUR - in EUR/USD,
        USD in USD/JPY, GBP - in GBP/USD, and so on).	

        Returns: string

        """
        row = self._find_row(offer_id)
        if row:
            return row.getContractCurrency()

    def get_digits(self, offer_id):
        """
        The price precision of the instrument. It defines number of digits after
        the decimal point in the instrument price quote. For example, it is 5
        for EUR/USD and 3 for USD/JPY. Therefore, price for EUR/USD instrument
        may look like 1.33187, for USD/JPY instrument like 77.953.

        Returns: integer

        """
        row = self._find_row(offer_id)
        if row:
            return row.getDigits()

    def get_point_size(self, offer_id):
        """
        The size of one pip. It used to define the smallest move the instrument 
        can make. In the case of FX instruments, it is expressed in the 
        instrument counter currency. In the case of CFD instruments, it is
        expressed in the instrument 
        native currency. 
        
        The possible values are:	
            
        1.0;	
            
        0.1;	
            
        0.01;	
            
        0.001;	
            
        0.0001;	
            
        0.00001.
        
        Different instruments have different pip values.
        For example, it is 0.0001 for EUR/USD and 0.01 for USD/JPY.	
	
        Note: For different instruments, the minimum possible change of the
        price could be 1 pip or a fraction of 1 pip. In the case of FX
        instruments, the pip is the minimal possible change of the second-to-last
        digit in a price quote. In the case of CFD instruments, the pip is the
        minimal possible change of the last digit in a price quote.	

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getPointSize()

    def get_subscription_status(self, offer_id):
        """
        The subscription status.	
            
        The possible values are:	
        T	Available for trading.
        D	Disabled (applicable for the trading station only; orders can
                still be created, and D changes to T).
        V	View only.

        Returns: string

        """
        row = self._find_row(offer_id)
        if row:
            return row.getSubscriptionStatus()

    def get_trading_status(self, offer_id):
        """
        The trading status.	
            
        The possible values are:	
        O	Open, in other words, the instrument is tradable.
        C	Closed, in other words, the instrument is not tradable.

        Returns: string

        """
        row = self._find_row(offer_id)
        if row:
            return row.getTradingStatus()

    def get_instrument_type(self, offer_id):
        """
        The type of the instrument. The possible values are:	
        1	Forex.
        2	Indices.
        3	Commodity.
        4	Treasury.
        5	Bullion.
        6	Shares.
        7	FXIndex.

        Returns: integer

        """
        row = self._find_row(offer_id)
        if row:
            return row.getInstrumentType()

    def get_contract_multiplier(self, offer_id):
        """
        The contract multiplier for some CFD instruments only. It is used for 
        simulation of the real-life trading conditions. For example, it is
        impossible to buy less than 25,000 lbs of copper on the market. 
        Hence, the value of 
        this field for Copper is 25000. In the case of FX instruments, the 
        value of this field is 1.	

        Returns: integer

        """
        row = self._find_row(offer_id)
        if row:
            return row.getContractMultiplier()

    def get_value_date(self, offer_id):
        """
        The simulated delivery date. The date and time when the position 
        opened in the instrument could be automatically closed. The value 
        of this field is provided in the yyyyMMdd format. It is applicable
        only when instrument trades on account with the day netting trading
        mode (see MaintenanceType field in the Accounts table). Otherwise,
        the value of this field is blank.	

        Returns: string

        """
        row = self._find_row(offer_id)
        if row:
            return row.getValueDate()

    def get_time(self, offer_id):
        """
        The date and time of the last update of the instrument. The time zone is 
        defined by the system propertiesSERVER_TIME_UTC and BASE_TIME_ZONE.	

        Returns: date

        """
        row = self._find_row(offer_id)
        if row:
            return row.getTime()

##    def get_pip_cost(self, offer_id):
##        """
#        The cost of one pip per lot. It is expressed in the account currency 
#        and used to calculate the P/L value in the account currency. The 
#        size of one lot is returned by the getBaseUnitSize method of the 
#        TradingSettingsProvider object.	
#        
#        Note: It is a calculated field and is available only through the Table
#        Manager.	
#
#        Returns: double
#        
#        #"""
##        row = self._find_row(offer_id)
##        if row:
##            return row.getPipCost()

    def is_offer_id_valid(self, offer_id):
        """
        Gets the flag indicating whether the OfferID field is valid.
        """
        row = self._find_row(offer_id)
        if row:
            return row.isOfferIDValid()

    def is_instrument_valid(self, offer_id):
        """
        Gets the flag indicating whether the Instrument field is valid.
        """
        row = self._find_row(offer_id)
        if row:
            return row.isInstrumentValid()

    def is_quote_id_valid(self, offer_id):
        """
        Gets the flag indicating whether the QuoteID field is valid.
        """
        row = self._find_row(offer_id)
        if row:
            return row.isQuoteIDValid()

    def is_bid_valid(self, offer_id):
        """
        Gets the flag indicating whether the Bid field is valid or not.
        """
        row = self._find_row(offer_id)
        if row:
            return row.isBidValid()

    def is_ask_valid(self, offer_id):
        """
        Gets the flag indicating whether the Ask field is valid or not.
        """
        row = self._find_row(offer_id)
        if row:
            return row.isAskValid()

    def is_low_valid(self, offer_id):
        """
        Gets the flag indicating whether the Low field is valid
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isLowValid()

    def is_high_valid(self, offer_id):
        """
        Gets the flag indicating whether the High field is valid or not.
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isHighValid()

    def is_volume_valid(self, offer_id):
        """
        Gets the flag indicating whether the Volume field is valid or not.
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isVolumeValid()

    def is_time_valid(self, offer_id):
        """
        Gets the flag indicating whether the date and time of the last
        instument update is valid or not.
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isTimeValid()

    def is_bid_tradable_valid(self, offer_id):
        """
        Gets the flag indicating whether the BidTradable field is valid or not.
        """
        row = self._find_row(offer_id)
        if row:
            return row.isBidTradableValid()

    def is_ask_tradable_valid(self, offer_id):
        """
        Gets the flag indicating whether the AskTradable field is valid or not.
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isAskTradableValid()

    def is_sell_interest_valid(self, offer_id):
        """
        Gets the flag indicating whether the SellInterest field is valid or not.
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isSellInterestValid()

    def is_buy_interest_valid(self, offer_id):
        """
        Gets the flag indicating whether the BuyInterest field is valid or not.
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isBuyInterestValid()

    def is_contract_currency_valid(self, offer_id):
        """
        Gets the flag indicating whether the ContractCurrency field is
        valid or not.
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isContractCurrencyValid()

    def is_digits_valid(self, offer_id):
        """
        Gets the flag indicating whether the Digits field is valid or not.
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isDigitsValid()

    def is_point_size_valid(self, offer_id):
        """
        Gets the flag indicating whether the PointSize field is valid or not.
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isPointSizeValid()

    def is_subscription_status_valid(self, offer_id):
        """
        Gets the flag indicating whether the SubscriptionStatus field
        is valid or not.
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isSubscriptionStatusValid()

    def is_instrument_type_valid(self, offer_id):
        """
        Gets the flag indicating whether the InstrumentType field is valid 
        or not.
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isInstrumentTypeValid()

    def is_contract_multiplier_valid(self, offer_id):
        """
        Gets the flag indicating whether the ContractMultiplier field is
        valid or not.
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isContractMultiplierValid()

    def is_trading_status_valid(self, offer_id):
        """
        Gets the flag indicating whether the TradingStatus field is 
        valid or not.
        """
        row = self._find_row(offer_id)
        if row:
            return row.isTradingStatusValid()

    def is_value_date_valid(self, offer_id):
        """
        Gets the flag indicating whether the ValueDate field is valid or not.
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.isValueDateValid()