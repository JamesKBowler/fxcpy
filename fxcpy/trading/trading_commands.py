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
from forexconnect import O2GRequestParamsEnum as O2G

from ..logger import Log
log = Log().logger

class TradingCommands(object):
    def __init__(
        self, session, account_id, offer_attribs
    ):
        """
        
        """
        log.debug("")
        self._offer_attribs = offer_attribs
        self.account_id = account_id
        self._session = session
        session.addRef()
        self._request_factory = session.getRequestFactory()

    def _get_base_unit(self, offer_id):
        """
        Returns: base_unit delta for the instrument
        """
        return self._offer_attribs[offer_id]
    
    def _send_request(self, valuemap):
        """
        Send order request to the trading server.
        """
        log.debug("")
        if not self._request_factory:
            raise NameError("Cannot find Request Factory")
        request = self._request_factory.createOrderRequest(valuemap)
        if not request:
            raise ValueError("Request Factory error: {}".format(
                self._request_factory.getLastError())
            )
        self._session.sendRequest(request)
        
    def create_valuemap(self, valuemap_type="CreateOrder"):
        """
        Returns: IO2GValuemap.
        """
        supported_valuemaps = [
            'CreateOrder',
            'CreateOCO',
            'CreateOTO',
            'EditOrder',
            'DeleteOrder',
            'JoinToNewContingencyGroup',
            'RemoveFromContingencyGroup',
            'GetLastOrderUpdate',
            'UpdateMarginRequirements',
            'AcceptOrder',
            'ChangePassword']
        if valuemap_type not in supported_valuemaps:
            raise AttributeError(
                "valuemap_type must be either {}".format(supported_valuemaps))
                
        valuemap = self._request_factory.createValueMap()
        if not valuemap:
            raise NameError("Cannot create valuemap")
        
        valuemap.setString(O2G.Command, valuemap_type)
        return valuemap
        
    def set_subscription_status(self, offer_id, status='T'):
        """
        Subscription status.
        Possible values are:
            "T" (enabled)
            "V" (hidden)
            "D" (disabled)
        """
        if not isinstance(offer_id, str):
            raise AttributeError('offer_id must be an string')
        try:
            int(offer_id)
        except:
            raise AttributeError('offer_id must be an string integer')
        
        if status not in ['T','V','D']:
            raise AttributeError("status must be either T, V or D")
        
        valuemap = self.create_valuemap("SetSubscriptionStatus")
        valuemap.setString(O2G.OfferID, offer_id)
        valuemap.setString(O2G.SubscriptionStatus, status)
        self._send_request(valuemap)
        
    def execute_order(self, valuemap):
        """
        Send order for execution
        """
        log.debug("")
        self._send_request(valuemap)
        log.info("Request has been sent to the execution server")
        
    def create_open_market_order(
        self,
        offer_id,
        buysell,
        amount,
        custom_id="TrueMarketOpen",
        time_in_force="IOC"):
        """
        An open market order opens a position at any currently available 
        market rate.
        
        If hedging is disabled for the account, the command, first, closes
        existing opposite positions for the same account and instrument and
        only then opens a new position in the remaining amount.
        
        Returns: valuemap
        """
        log.debug("")
        
        if not isinstance(offer_id, str):
            raise AttributeError('offer_id must be an string')
        try:
            int(offer_id)
        except:
            raise AttributeError('offer_id must be an string integer')
        
        if buysell not in ['B','S']:
            raise AttributeError('buysell must be either string B or S')
        
        if not isinstance(amount, int):
            raise AttributeError('amount must be a integer')

        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')

        if time_in_force not in ['IOC', 'GTC', 'FOK', 'DAY', 'GTD']:
            raise AttributeError(
                "time_in_force must be either IOC, GTC, FOK, DAY, GTD")
        
        valuemap = self.create_valuemap()
        valuemap.setString(O2G.OrderType, "OM")
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.OfferID, offer_id)
        valuemap.setString(O2G.BuySell, buysell)
        valuemap.setString(O2G.TimeInForce, time_in_force)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setInt(O2G.Amount, amount * self._get_base_unit(offer_id))
        return valuemap

    def create_open_order(
        self,
        offer_id,
        buysell,
        amount,
        rate,
        custom_id="MarketOpen",
        time_in_force="IOC"):
        """
        An open order opens a position at the specified market rate in 
        case such rate is available on the market.
        
        If hedging is disabled for the account, the command, first, closes
        existing opposite positions for the same account and instrument and
        only then opens a new position in the remaining amount.
        
        Returns: valuemap
        """
        log.debug("")
        
        if not isinstance(offer_id, str):
            raise AttributeError('offer_id must be an string')
        try:
            int(offer_id)
        except:
            raise AttributeError('offer_id must be an string integer')
        
        if buysell not in ['B','S']:
            raise AttributeError('buysell must be either string B or S')
        
        if not isinstance(amount, int):
            raise AttributeError('amount must be a integer')
        
        if not isinstance(rate, float):
            raise AttributeError('rate must be a float')

        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')

        if time_in_force not in ['IOC', 'FOK']:
            raise AttributeError(
                "time_in_force must be either IOC, FOK")
                
        valuemap = self.create_valuemap()
        valuemap.setString(O2G.OrderType, "O")
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.OfferID, offer_id)
        valuemap.setString(O2G.BuySell, buysell)
        valuemap.setString(O2G.TimeInForce, time_in_force)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setInt(O2G.Amount, amount * self._get_base_unit(offer_id))
        valuemap.setDouble(O2G.Rate, rate)
        return valuemap
            
    def create_open_limit_order(
        self, offer_id,
        buysell,
        amount,
        rate,
        custom_id="OpenLimit",            
        time_in_force="IOC"):
        """
        An open order opens a position at the specified market rate or at 
        a more favorable rate in case such rate is available on the market.
        
        If hedging is disabled for the account, the command, first, closes
        existing opposite positions for the same account and instrument and
        only then opens a new position in the remaining amount.
        
        Returns: valuemap
        """
        log.debug("")
        
        if not isinstance(offer_id, str):
            raise AttributeError('offer_id must be an string')
        try:
            int(offer_id)
        except:
            raise AttributeError('offer_id must be an string integer')
        
        if buysell not in ['B','S']:
            raise AttributeError('buysell must be either string B or S')
        
        if not isinstance(amount, int):
            raise AttributeError('amount must be a integer')
        
        if not isinstance(rate, float):
            raise AttributeError('rate must be a float')

        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')

        if time_in_force not in ['IOC', 'FOK']:
            raise AttributeError(
                "time_in_force must be either IOC, FOK")
                
        valuemap = self.create_valuemap()
        valuemap.setString(O2G.OrderType, "OL")
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.OfferID, offer_id)
        valuemap.setString(O2G.BuySell, buysell)
        valuemap.setString(O2G.TimeInForce, time_in_force)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setInt(O2G.Amount, amount * self._get_base_unit(offer_id))
        valuemap.setDouble(O2G.Rate, rate)
        return valuemap
            
    def create_open_range_order(
        self, offer_id,
        buysell, 
        amount,
        rate_min, 
        rate_max,
        custom_id="MarketOpenRange",
        time_in_force="IOC"):
        """
        An open range order opens a position at the available market rate 
        in case this rate is in the range specified in the command.
        
        If hedging is disabled for the account, the command, first, closes
        existing opposite positions for the same account and instrument and
        only then opens a new position in the remaining amount.
        
        Returns: valuemap
        """
        log.debug("")

        if not isinstance(offer_id, str):
            raise AttributeError('offer_id must be an string')
        try:
            int(offer_id)
        except:
            raise AttributeError('offer_id must be an string integer')
        
        if buysell not in ['B','S']:
            raise AttributeError('buysell must be either string B or S')
        
        if not isinstance(amount, int):
            raise AttributeError('amount must be a integer')
        
        if not isinstance(rate_min, float):
            raise AttributeError('rate_min must be a float')
        
        if not isinstance(rate_max, float):
            raise AttributeError('rate_max must be a float')

        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')

        if time_in_force not in ['IOC', 'FOK']:
            raise AttributeError(
                "time_in_force must be either IOC, FOK")
                
        valuemap = self.create_valuemap()
        valuemap.setString(O2G.OrderType, "OR")
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.OfferID, offer_id)
        valuemap.setString(O2G.BuySell, buysell)
        valuemap.setString(O2G.TimeInForce, time_in_force)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setInt(O2G.Amount, amount * self._get_base_unit(offer_id))
        valuemap.setDouble(O2G.RateMin, rate_min)
        valuemap.setDouble(O2G.RateMax, rate_max)
        return valuemap

    def create_close_market_order(
        self,
        offer_id,
        buysell,
        trade_id=None,
        amount=0,
        custom_id="TrueMarketClose",
        net_quantity="Y",
        time_in_force="IOC"):
        """
        A close market order closes a position at any currently available 
        market rate.

        Note:
        # Close orders must be permitted for the account in order to be used.
        # Netting close order can be executed even if close orders are disabled.
        
        Returns: valuemap
        """
        log.debug("")
        
        if not isinstance(offer_id, str):
            raise AttributeError('offer_id must be an string')
        try:
            int(offer_id)
        except:
            raise AttributeError('offer_id must be an string integer')
        
        if buysell not in ['B','S']:
            raise AttributeError('buysell must be either string B or S')
        
        if trade_id is not None:
            if not isinstance(trade_id, str):
                raise AttributeError('trade_id must be a string')
            try:
                int(trade_id)
            except:
                raise AttributeError('trade_id must be an string integer')

        if not isinstance(amount, int):
            raise AttributeError('amount must be a integer')
        
        if net_quantity not in ['Y', 'N']:
            raise AttributeError('net_quantity must be a Y or N')

        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')

        if time_in_force not in ['IOC', 'GTC', 'FOK', 'DAY', 'GTD']:
            raise AttributeError(
                "time_in_force must be either IOC, GTC, FOK, DAY, GTD")        
        
        valuemap = self.create_valuemap()
        valuemap.setString(O2G.OrderType, "CM")
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.OfferID, offer_id)
        if net_quantity == "Y":
            if buysell is None:
                raise AttributeError(
                    "Net Quantity Order requires a target 'S' to close all "
                    "LONG poistions or 'B' to close all SHORT positions")
        else:
            if trade_id is None:
                raise AttributeError(
                    "None Net Quantity Order requires a trade_id")
            else:
                valuemap.setString(O2G.TradeID, trade_id)
                if amount == 0:
                    raise AttributeError(
                        "Must enter an amount for none NET orders")
                else:
                    valuemap.setInt(O2G.Amount, amount)
        valuemap.setString(O2G.BuySell, buysell)
        valuemap.setString(O2G.TimeInForce, time_in_force)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setString(O2G.NetQuantity, net_quantity)
        return valuemap
            
    def create_close_order(
        self,
        offer_id,
        buysell=None,
        trade_id=None,
        amount=0,
        custom_id="MarketClose",
        net_quantity="Y",
        time_in_force="IOC"):
        """
        A close order closes a position at the specified market rate in case 
        such rate is available on the market.

        Note:
        # Close orders must be permitted for the account in order to be used.
        
        Returns: valuemap
        """
        log.debug("")
        
        if not isinstance(offer_id, str):
            raise AttributeError('offer_id must be an string')
        try:
            int(offer_id)
        except:
            raise AttributeError('offer_id must be an string integer')
        
        if buysell is not None and buysell not in ['B','S']:
            raise AttributeError('buysell must be either string B or S')
        
        if trade_id is not None:
            if not isinstance(trade_id, str):
                raise AttributeError('trade_id must be a string')
            try:
                int(trade_id)
            except:
                raise AttributeError('trade_id must be an string integer')

        if not isinstance(amount, int):
            raise AttributeError('amount must be a integer')
        
        if net_quantity not in ['Y', 'N']:
            raise AttributeError('net_quantity must be a Y or N')

        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')

        if time_in_force not in ['IOC', 'FOK']:
            raise AttributeError(
                "time_in_force must be either IOC, FOK")  
                
        valuemap = self.create_valuemap()
        valuemap.setString(O2G.OrderType, "C")
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.OfferID, offer_id)
        valuemap.setDouble(O2G.Rate, rate)
        if net_quantity == "Y":
            if buysell is None:
                raise AttributeError(
                    "Net Quantity Order requires a target 'S' to close all "
                    "LONG poistions or 'B' to close all SHORT positions"
                )
        else:
            if trade_id is None:
                raise AttributeError(
                    "None Net Quantity Order requires a trade_id"
                )
            else:
                valuemap.setString(O2G.TradeID, trade_id)
                if amount == 0:
                    raise AttributeError(
                        "Must enter an amount for none NET orders")
                else:
                    valuemap.setInt(O2G.Amount, amount * self._get_base_unit(offer_id))
        valuemap.setString(O2G.BuySell, buysell)
        valuemap.setString(O2G.TimeInForce, time_in_force)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setString(O2G.NetQuantity, net_quantity)
        return valuemap

    def create_close_limit_order(
        self,
        offer_id,
        rate,
        buysell=None,
        trade_id=None,
        amount=0,
        custom_id="CloseLimit",
        net_quantity="Y",
        time_in_force="IOC"):
        """
        A close order closes a position at the specified market rate or at 
        a more favorable price in case such rate is available on the market.
        
        Note:
        # Close orders must be permitted for the account in order to be used.
        
        Returns: valuemap
        """
        log.debug("")
        
        if not isinstance(offer_id, str):
            raise AttributeError('offer_id must be an string')
        try:
            int(offer_id)
        except:
            raise AttributeError('offer_id must be an string integer')
        
        if buysell is not None and buysell not in ['B','S']:
            raise AttributeError('buysell must be either string B or S')
        
        if trade_id is not None:
            if not isinstance(trade_id, str):
                raise AttributeError('trade_id must be a string')
            try:
                int(trade_id)
            except:
                raise AttributeError('trade_id must be an string integer')

        if not isinstance(amount, int):
            raise AttributeError('amount must be a integer')
        
        if net_quantity not in ['Y', 'N']:
            raise AttributeError('net_quantity must be a Y or N')

        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')

        if time_in_force not in ['IOC', 'FOK']:
            raise AttributeError(
                "time_in_force must be either IOC, FOK")  
                
        valuemap = self.create_valuemap()
        valuemap.setString(O2G.OrderType, "CL")
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.OfferID, offer_id)
        valuemap.setDouble(O2G.Rate, rate)
        if net_quantity == "Y":
            if buysell is None:
                raise AttributeError(
                    "Net Quantity Order requires a target 'S' to close all "
                    "LONG poistions or 'B' to close all SHORT positions"
                )
        else:
            if trade_id is None:
                raise AttributeError(
                    "None Net Quantity Order requires a trade_id"
                )
            else:
                valuemap.setString(O2G.TradeID, trade_id)
                if amount == 0:
                    raise AttributeError(
                        "Must enter an amount for none NET orders")
                else:
                    valuemap.setInt(O2G.Amount, amount * self._get_base_unit(offer_id))
        valuemap.setString(O2G.BuySell, buysell)
        valuemap.setString(O2G.TimeInForce, time_in_force)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setString(O2G.NetQuantity, net_quantity)
        return valuemap
            
    def create_close_range_order(
        self,
        offer_id,
        rate_min, 
        rate_max,
        buysell=None,
        trade_id=None,
        amount=0,
        custom_id="MarketCloseRange",
        net_quantity="Y",
        time_in_force="IOC"):
        """
        A close range order closes a position at the available market rate 
        in case this rate is in the range specified in the command.
        
        Note:
        # Close orders must be permitted for the account in order to be used.
        
        Returns: valuemap
        """
        log.debug("")

        if not isinstance(offer_id, str):
            raise AttributeError('offer_id must be an string')
        try:
            int(offer_id)
        except:
            raise AttributeError('offer_id must be an string integer')
        
        if not isinstance(rate_min, float):
            raise AttributeError('rate_min must be a float')
        
        if not isinstance(rate_max, float):
            raise AttributeError('rate_max must be a float')
        
        if buysell is not None and buysell not in ['B','S']:
            raise AttributeError('buysell must be either string B or S')
        
        if trade_id is not None:
            if not isinstance(trade_id, str):
                raise AttributeError('trade_id must be a string')
            try:
                int(trade_id)
            except:
                raise AttributeError('trade_id must be an string integer')

        if not isinstance(amount, int):
            raise AttributeError('amount must be a integer')
        
        if net_quantity not in ['Y', 'N']:
            raise AttributeError('net_quantity must be a Y or N')

        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')

        if time_in_force not in ['IOC', 'FOK']:
            raise AttributeError(
                "time_in_force must be either IOC, FOK") 

        valuemap = self.create_valuemap()
        valuemap.setString(O2G.OrderType, "CR")
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.OfferID, offer_id)
        valuemap.setDouble(O2G.RateMin, rate_min)        
        valuemap.setDouble(O2G.RateMax, rate_max)
        if net_quantity == "Y":
            if buysell is None:
                raise AttributeError(
                    "Net Quantity Order requires a target 'S' to close all "
                    "LONG poistions or 'B' to close all SHORT positions"
                )
        else:
            if trade_id is None:
                raise AttributeError(
                    "None Net Quantity Order requires a trade_id"
                )
            else:
                valuemap.setString(O2G.TradeID, trade_id)
                if amount == 0:
                    raise AttributeError(
                        "Must enter an amount for none NET orders")
                else:
                    valuemap.setInt(O2G.Amount, amount * self._get_base_unit(offer_id))
        valuemap.setString(O2G.BuySell, buysell)
        valuemap.setString(O2G.TimeInForce, time_in_force)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setString(O2G.NetQuantity, net_quantity)
        return valuemap
            
    def create_entry_limit_order(
        self,
        offer_id, 
        buysell,
        rate,
        contingency_id, 
        contingency_group_type,
        amount=0,
        trail_step=0,
        custom_id="LimitEntry",
        net_quantity="Y",
        time_in_force="GTC"):
        """
        A regular entry order opens a position when the specified market
        condition is met. Netting entry orders close all positions for the
        specified instrument and account which are in the direction
        (buy or sell) opposite to the direction of the entry order.

        Orders in a sell direction are filled when the market is above
        the rate specified in the order.
        Orders in a buy direction are filled when the market is below the
        rate specified in the order.

        If hedging is disabled for the account, the command, first, closes
        existing opposite positions for the same account and instrument and
        only then opens a new position in the remaining amount.
        
        Returns: valuemap
        """
        log.debug("")
        
        if not isinstance(offer_id, str):
            raise AttributeError('offer_id must be an string')
        try:
            int(offer_id)
        except:
            raise AttributeError('offer_id must be an string integer')
        
        if not isinstance(rate, float):
            raise AttributeError('rate_min must be a float')
        
        if buysell is not None and buysell not in ['B','S']:
            raise AttributeError('buysell must be either string B or S')
        
        if not isinstance(contingency_id, str):
            raise AttributeError('contingency_id must be a string integer')
        
        if not isinstance(contingency_group_type, int):
            raise AttributeError('contingency_group_type must be a integer')
        
        if not isinstance(amount, int):
            raise AttributeError('amount must be a integer')

        if not isinstance(trail_step, int):
            raise AttributeError('trail_step must be a integer')
        
        if net_quantity not in ['Y', 'N']:
            raise AttributeError('net_quantity must be a Y or N')

        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')

        if time_in_force not in ['GTC', 'DAY', 'GTD']:
            raise AttributeError(
                "time_in_force must be either GTC, DAY, GTD")

        valuemap = self.create_valuemap()
        valuemap.setString(O2G.OrderType, "LE")
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.OfferID, offer_id)
        valuemap.setString(O2G.BuySell, buysell)
        valuemap.setString(O2G.TimeInForce, time_in_force)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setDouble(O2G.Rate, rate)
        valuemap.setInt(O2G.TrailStep, trail_step)
        valuemap.setString(O2G.ContingencyID, contingency_id)
        valuemap.setInt(O2G.ContingencyGroupType, contingency_group_type)
        if net_quantity == "N":
            if amount == 0:
                raise AttributeError(
                    "Must enter an amount for none NET orders")
            else:
                valuemap.setInt(O2G.Amount, amount * self._get_base_unit(offer_id))
        return valuemap

    def create_entry_stop_order(
        self,
        offer_id, 
        buysell,
        rate,
        contingency_id, 
        contingency_group_type,
        amount=0,
        trail_step=0,
        custom_id="StopEntry",
        net_quantity="Y",
        time_in_force="GTC"):
        """
        Regular entry orders open a position when the specified market
        condition is met. Netting entry orders close all positions for the
        specified instrument and account which are in the direction
        (buy or sell) opposite to the direction of the entry order.
        
        Orders with a sell direction is filled when the market is below the
        rate specified in the order.
        
        Orders with a buy direction is filled when the market is above the
        rate specified in the order.

        If hedging is disabled for the account, the command, first, closes
        existing opposite positions for the same account and instrument and
        only then opens a new position in the remaining amount.
        
        Returns: valuemap
        """
        log.debug("")
        
        if not isinstance(offer_id, str):
            raise AttributeError('offer_id must be an string')
        try:
            int(offer_id)
        except:
            raise AttributeError('offer_id must be an string integer')
        
        if not isinstance(rate, float):
            raise AttributeError('rate_min must be a float')
        
        if buysell is not None and buysell not in ['B','S']:
            raise AttributeError('buysell must be either string B or S')
        
        if not isinstance(contingency_id, str):
            raise AttributeError('contingency_id must be a string integer')
        
        if not isinstance(contingency_group_type, int):
            raise AttributeError('contingency_group_type must be a integer')
        
        if not isinstance(amount, int):
            raise AttributeError('amount must be a integer')

        if not isinstance(trail_step, int):
            raise AttributeError('trail_step must be a integer')

        if net_quantity not in ['Y', 'N']:
            raise AttributeError('net_quantity must be a Y or N')

        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')

        if time_in_force not in ['GTC', 'DAY', 'GTD']:
            raise AttributeError(
                "time_in_force must be either GTC, DAY, GTD")  
                
        valuemap = self.create_valuemap()
        valuemap.setString(O2G.OrderType, "SE")
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.OfferID, offer_id)
        valuemap.setString(O2G.BuySell, buysell)
        valuemap.setString(O2G.TimeInForce, time_in_force)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setDouble(O2G.Rate, rate)
        valuemap.setInt(O2G.TrailStep, trail_step)
        valuemap.setString(O2G.ContingencyID, contingency_id)
        valuemap.setInt(O2G.ContingencyGroupType, contingency_group_type)
        if net_quantity == "N":
            if amount == 0:
                raise AttributeError(
                    "Must enter an amount for none NET orders")
            else:
                valuemap.setInt(O2G.Amount, amount * self._get_base_unit(offer_id))
        return valuemap
            
    def create_entry_order(
        self,
        offer_id, 
        buysell, 
        amount,
        rate,
        contingency_id,
        contingency_group_type,
        trail_step=0,
        custom_id="Entry",
        net_quantity="Y",
        time_in_force="GTC"):
        """
        A regular entry order opens a position when the specified market
        condition is met.
        Please note that if hedging is disabled for the account, the order,
        first, closes existing opposite positions for the same account and
        instrument and only then opens a new position for the remaining amount.

        A netting entry order closes all positions for the specified instrument
        and account which are in the direction (buy or sell) opposite to the 
        direction of the entry order.

        There are two types of Entry orders : Limit Entry and Stop Entry. 
        This command allows you to create an entry order without specifying 
        order type. The system will determine order type automatically, based 
        on three parameters:

        Order direction (Buy or Sell).

        Desired order rate.

        Current market price of a trading instrument.

        The system will create a Limit Entry order if:
         # Rate for a buy order is below current market price.
         # Rate for a sell order is above current market price.
        
        The system will create a Stop Entry order if:
         # Rate for a buy order is above current market price.
         # Rate for a sell order is below current market price.

        Note: This command only available when using IO2GTableManager.

        Returns: valuemap
        """
        log.debug("")
        
        if not isinstance(offer_id, str):
            raise AttributeError('offer_id must be an string')
        try:
            int(offer_id)
        except:
            raise AttributeError('offer_id must be an string integer')
        
        if not isinstance(rate, float):
            raise AttributeError('rate_min must be a float')
        
        if buysell is not None and buysell not in ['B','S']:
            raise AttributeError('buysell must be either string B or S')
        
        if not isinstance(contingency_id, str):
            raise AttributeError('contingency_id must be a string integer')
        
        if not isinstance(contingency_group_type, int):
            raise AttributeError('contingency_group_type must be a integer')
        
        if not isinstance(amount, int):
            raise AttributeError('amount must be a integer')

        if not isinstance(trail_step, int):
            raise AttributeError('trail_step must be a integer')

        if net_quantity not in ['Y', 'N']:
            raise AttributeError('net_quantity must be a Y or N')

        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')

        if time_in_force not in ['GTC', 'DAY', 'GTD']:
            raise AttributeError(
                "time_in_force must be either GTC, DAY, GTD")  
                
        valuemap = self.create_valuemap()
        valuemap.setString(O2G.OrderType, "E")
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.OfferID, offer_id)
        valuemap.setString(O2G.BuySell, buysell)
        valuemap.setString(O2G.TimeInForce, time_in_force)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setString(O2G.NetQuantity, net_quantity)
        valuemap.setDouble(O2G.Rate, rate)
        valuemap.setInt(O2G.TrailStep, trail_step) 
        valuemap.setString(O2G.ContingencyID, contingency_id)
        valuemap.setInt(O2G.ContingencyGroupType, contingency_group_type)
        if net_quantity == "N":
            if amount == 0:
                raise AttributeError(
                    "Must enter an amount for none NET orders")
            else:
                valuemap.setInt(O2G.Amount, amount * self._get_base_unit(offer_id))
        return valuemap
            
    def create_limit_order(
        self,
        offer_id,
        trade_id,
        buysell,
        amount,
        rate=None,
        peg_type="M", 
        peg_offset=None,
        custom_id="Limit",
        time_in_force="GTC"):
        """
        A limit order is used for locking in profit of the existing position 
        when the market condition is met.
        Limit orders can be created for existing trades as well as for existing 
        entry orders. Limit orders created for entry orders remain inactive until
        the trade is created by the entry order.
        
        Only one limit order can be attached to a position or an entry order.
        
        Note:
         # Close orders must be permitted for the account in order to be used.
         # Stop and limit orders cannot be attached to netting entry orders.

        Returns: valuemap
        """
        log.debug("")

        if not isinstance(trade_id, str):
            raise AttributeError('trade_id must be an string')
        try:
            int(trade_id)
        except:
            raise AttributeError('trade_id must be an string integer')
        
        if buysell is not None and buysell not in ['B','S']:
            raise AttributeError('buysell must be either string B or S')

        if not isinstance(amount, int):
            raise AttributeError('amount must be a integer')
        
        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')

        if time_in_force not in ['GTC', 'DAY', 'GTD']:
            raise AttributeError(
                "time_in_force must be either GTC, DAY, GTD")  
                
        if rate is None and peg_offset is None:
            raise AttributeError("Must set a rate or peg amount")
        
        valuemap = self.create_valuemap()
        valuemap.setString(O2G.OrderType, "L")
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.OfferID, offer_id)
        valuemap.setString(O2G.BuySell, buysell)
        valuemap.setString(O2G.TimeInForce, time_in_force)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setInt(O2G.Amount, amount)
        valuemap.setString(O2G.TradeID, trade_id)
        if rate is not None and peg_offset is None:
            if not isinstance(rate, float):
                raise AttributeError('rate_min must be a float')
            valuemap.setDouble(O2G.Rate, rate)
        elif rate is None and peg_offset is not None: 
            if not isinstance(peg_offset, float):
                raise AttributeError('peg_offset must be a float')
            valuemap.setDouble(O2G.PegOffset, peg_offset)
            if peg_type not in ['O', 'M']:
                raise AttributeError("peg_type must be either O or M") 
            valuemap.setString(O2G.PegType, peg_type)
        else:
            raise AttributeError(
                "Cannot be both, must set a rate "
                "or peg amount in pips"
            )
        return valuemap
            
    def create_stop_order(
        self,
        offer_id,
        trade_id,
        buysell,
        amount,
        rate=None,
        peg_type="M",
        peg_offset=None,
        trail_step=0,
        custom_id="Stop",
        time_in_force="GTC"):
        """
        A stop order is used for limiting losses of the existing position when
        the market condition is met.
        Stop orders can be created for existing trades as well as for existing
        entry orders. Stop orders created for entry orders remain inactive until
        the trade is created by the entry order.

        Only one stop order can be attached to a position or an the entry order.
        
        Note:
         # Close orders must be permitted for the account in order to be used.
         # Stop and limit orders cannot be attached to netting entry orders.

        Returns: valuemap
        """
        log.debug("")
        if not isinstance(trade_id, str):
            raise AttributeError('trade_id must be an string')
        try:
            int(trade_id)
        except:
            raise AttributeError('trade_id must be an string integer')
        
        if buysell is not None and buysell not in ['B','S']:
            raise AttributeError('buysell must be either string B or S')

        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')
        
        if not isinstance(amount, int):
            raise AttributeError('amount must be a integer')
        
        if time_in_force not in ['GTC', 'DAY', 'GTD']:
            raise AttributeError(
                "time_in_force must be either IOC, GTC, FOK, DAY, GTD")  
                
        if rate is None and peg_offset is None:
            raise AttributeError("Must set a rate or peg amount")
            
        valuemap = self.create_valuemap()
        valuemap.setString(O2G.OrderType, "S")
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.OfferID, offer_id)
        valuemap.setString(O2G.BuySell, buysell)
        valuemap.setInt(O2G.Amount, amount)
        valuemap.setInt(O2G.TrailStep, trail_step) 
        valuemap.setString(O2G.TimeInForce, time_in_force)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setString(O2G.TradeID, trade_id)
        if rate is not None and peg_offset is None:
            if not isinstance(rate, float):
                raise AttributeError('rate_min must be a float')
            valuemap.setDouble(O2G.Rate, rate)
        elif rate is None and peg_offset is not None: 
            if not isinstance(peg_offset, float):
                raise AttributeError('peg_offset must be a float')
            valuemap.setDouble(O2G.PegOffset, peg_offset)
            if peg_type not in ['O', 'M']:
                raise AttributeError("peg_type must be either O or M") 
            valuemap.setString(O2G.PegType, peg_type)
        else:
            raise AttributeError(
                "Cannot be both, must set a rate "
                "or peg amount in pips"
            )
        return valuemap
            
    def edit_order(
        self,
        order_id,
        offer_id=None,
        amount=None,
        rate=None,
        peg_type="M", 
        peg_offset=None,
        trail_step=0,
        custom_id="EditOrder"):
        """
        Only Entry Stop (SE), Entry Limit (LE), Stop (S) and Limit (L) 
        orders (and all their modifications) in the Waiting ("W") state can 
        be changed.

        Returns: valuemap
        """
        log.debug("")
        if not isinstance(order_id, str):
            raise AttributeError('order_id must be an string')
        try:
            int(order_id)
        except:
            raise AttributeError('order_id must be an string integer')

        if not isinstance(custom_id, str):
            raise AttributeError('custom_id must be an string')

        valuemap = self.create_valuemap("EditOrder")
        valuemap.setString(O2G.OrderID, order_id)
        valuemap.setString(O2G.AccountID, self.account_id)
        valuemap.setString(O2G.CustomID, custom_id)
        valuemap.setInt(O2G.TrailStep, trail_step)
        if amount is not None:
            if offer_id is None:
                raise AttributeError('offer_id required to calc base_unit')
            if not isinstance(amount, int):
                raise AttributeError('amount must be a integer')
            valuemap.setInt(O2G.Amount, amount * self._get_base_unit(offer_id))
            if not isinstance(rate, float):
                raise AttributeError('rate_min must be a float')
            valuemap.setDouble(O2G.Rate, rate)
        elif peg_offset is not None:
            if not isinstance(peg_offset, float):
                raise AttributeError('peg_offset must be a float')
            valuemap.setDouble(O2G.PegOffset, peg_offset)
            if peg_type not in ['O', 'M']:
                raise AttributeError("peg_type must be either O or M") 
            valuemap.setString(O2G.PegType, peg_type)
        return valuemap
            
    def attach_stoplimit_orders(
        self,
        valuemap_index,
        master_valuemap,
        rate_stop=None,
        peg_type_stop="M", 
        peg_offset_stop=None,
        trail_step_stop=0, 
        rate_limit=None, 
        peg_type_limit="M",
        peg_offset_limit=None):
        """
        Orders which create a new position (OM, O, OR, SE and LE orders) 
        may also have additional values in the value map, which forces creating 
        associated stop and limit orders.

        Returns: valuemap
        """
        log.debug("")

        if master_valuemap.getChildrenCount() == 0:
            raise IndexError("Master valuemap is empty")

        if rate_stop is None and peg_offset_stop is None:
            raise AttributeError("Must set rate_limit or peg_offset_limit")
            
        if rate_limit is None and peg_offset_limit is None:
            raise AttributeError("Must set rate_stop or peg_offset_stop")
        
        if (rate_stop is not None and rate_limit is None or 
            rate_stop is None and rate_limit is not None):
            raise AttributeError("Must set rate_stop and rate_limit")

        if (peg_offset_stop is not None and peg_offset_limit is None or 
            peg_offset_stop is None and peg_offset_limit is not None):
            raise AttributeError("Must set peg_offset_stop and peg_offset_limit")
        
        valuemap = master_valuemap.getChild(valuemap_index)
        if not valuemap:
            raise IndexError("Child valuemap not found {}".format(valuemap_index))
        if rate_stop is not None:
            valuemap.setDouble(O2G.RateStop, rate_stop)
        else:
            valuemap.setDouble(O2G.PegTypeStop, peg_offset_stop)
            valuemap.setString(O2G.PegTypeStop, peg_type_stop)
        if rate_limit is not None:
            valuemap.setDouble(O2G.RateLimit, rate_limit)
        else:
            valuemap.setString(O2G.PegTypeLimit, peg_type_limit)
            valuemap.setString(O2G.PegOffsetLimit, peg_offset_limit)
        valuemap.setInt(O2G.TrailStep, trail_step_stop)
        return master_valuemap

    def delete_order(self, order_id):
        """
        Delete an order.

        Returns: valuemap
        """
        log.debug("")
        
        if not isinstance(order_id, str):
            raise AttributeError('order_id must be an string')
        try:
            int(order_id)
        except:
            raise AttributeError('order_id must be an string integer')
        
        valuemap = self.create_valuemap("DeleteOrder")
        valuemap.setString(O2G.OrderID, order_id)
        valuemap.setString(O2G.AccountID, self.account_id)
        return valuemap

    def create_new_contingency_group(self, contingency_type):
        """
        Join two or more existing entry orders into a new contingency 
        (OCO, OTO or ELS) group.
        The type of a new contingency group must be:
        OCO group : 1
        OTO group : 2
        ELS group : 3
        
        Returns: valuemap
        """
        log.debug("")
        
        if contingency_type not in [1,2,3]:
            raise AttributeError('contingency_type must be integer 1 ,2 or 3')
        
        valuemap = self.create_valuemap("JoinToNewContingencyGroup")
        valuemap.setInt(O2G.ContingencyGroupType, contingency_type)
        return valuemap
    
    def add_existing_orders_into_existing_contingency_group(
        self,
        group_id,
        contingency_type):
        """
        Add one or more existing entry order into an existing contingency 
        (OCO, OTO or ELS) group.

        Returns: valuemap
        """
        log.debug("")
        
        if contingencyType not in [1,2,3]:
            raise AttributeError('contingency_type must be integer 1 ,2 or 3')
        
        if not isinstance(group_id, str):
            raise AttributeError('group_id must be string integer')
        
        valuemap = self.create_valuemap("JoinToExistingContingencyGroup")
        valuemap.setString(O2G.ContingencyID, group_id)
        valuemap.setInt(O2G.ContingencyGroupType, contingency_type)
        return valuemap

    def remove_orders_from_existing_contingency_group(
        self,
        main_valuemap,
        valuemap_remove):
        """
        Remove one or more orders from an existing contingency (OCO, OTO or ELS) 
        group.

        Returns: valuemap
        """
        log.debug("")
        
        if main_valuemap.__name__ != "IO2GValueMap":
            raise AttributeError('main_valuemap must be IO2GValueMap')
        
        if valuemap_remove.__name__ != "IO2GValueMap":
            raise AttributeError('valuemap_remove must be IO2GValueMap')
        
        valuemap_remove.setString(O2G.Command, "RemoveFromContingencyGroup")
        main_valuemap.appendChild(valuemap_remove)
        return main_valuemap

    def update_margin_requirements(self):
        """
        This command is useful in case the instrument was not subscribed at
        the time of login but was subscribed later. It is used to get margin
        requirements for an instrument after subscribing to it.
        
        Returns: Nothing 
        """
        log.debug("")
        valuemap = self.create_valuemap("UpdateMarginRequirements")
        self._send_request(valuemap)

    def get_last_order_update(self, account_name, order_id):
        """
        Get the up-to-date order information from the server.
        
        Returns: Nothing
        
        """
        if not isinstance(account_name, str):
            raise AttributeError('account_name must be string')

        if not isinstance(order_id, str):
            raise AttributeError('order_id must be an string')
        try:
            int(order_id)
        except:
            raise AttributeError('order_id must be an string integer')
        
        valuemap = self.create_valuemap("GetLastOrderUpdate")
        valuemap.setString(O2G.AccountName, account_name)
        valuemap.setString(O2G.Key, O2G2.KeyType.OrderID)
        valuemap.setString(O2G.Id, order_id)
        self._send_request(valuemap)
         
    def accept_order(self, order_id):
        """
        Accept order requoted by the dealer.

        Returns: Nothing
        """
        log.debug("")
        
        if not isinstance(order_id, str):
            raise AttributeError('order_id must be an string')
        try:
            int(order_id)
        except:
            raise AttributeError('order_id must be an string integer')
        
        valuemap = self.create_valuemap("AcceptOrder")
        valuemap.setString(O2G.OrderID, order_id)
        self._send_request(valuemap)

    def change_password(self, new_password):
        """
        Change current password to a new one.
        
        Returns: Nothing 
        """
        log.debug("")
        
        if not isinstance(new_password, str):
            raise AttributeError('new_password must be string')
        
        valuemap = self.create_valuemap("ChangePassword")
        valuemap.setString(O2G.Psw, new_password)
        self._send_request(valuemap)