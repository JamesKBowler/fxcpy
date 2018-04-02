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
class TradingSettingsProvider(object):
    """
    TradingSettingsProvider    
    """
    def __init__(self, trading_settings_provider):
        self._b = trading_settings_provider
    
    def get_base_unit_size(self, instrument, account_row):
        """
        Gets the size of one lot, i.e. the minimum amount per trade that
        is allowed on the instrument on the account.

        Parameters:
            instrument : The name of the instrument to get the trading
                setting for.
            account_row : The account information for the account to
                get the trading setting for.
        
        Returns: int
                
        """
        return self._b._getBaseUnitSize(instrument, account_row)

    def get_cond_dist_entry_limit(self, instrument):
        """
        Gets the minimal distance between the rates of the entry limit
        order and the current market rate.

        Parameters:
            instrument : The name of the instrument to get the trading
                setting for.
        
        Returns:

        """
        return self._b._getCondDistEntryLimit(instrument)

    def get_cond_dist_entry_stop(self, instrument):
        """
        Gets the minimal distance between the rates of the entry stop
        order and the current market rate.

        Parameters:
            instrument : The name of the instrument to get the trading
                setting for.
        
        Returns:
                
        """
        return self._b._getCondDistEntryStop(instrument)

    def get_cond_dist_limit_for_trade(self, instrument):
        """
        Gets the minimal distance between the rates of the limit order 
        for the position and the current market rate.

        Parameters:
            instrument : The name of the instrument to get the trading
                setting for.
        
        Returns:

        """
        return self._b._getCondDistLimitForTrade(instrument)

    def get_cond_dist_stop_for_trade(self, instrument):
        """
        Gets the minimal distance between the rates of the stop order 
        for the position and the current market rate.

        Parameters:
            instrument : The name of the instrument to get the trading
                setting for.
        
        Returns:

        """
        return self._b._getCondDistStopForTrade(instrument)

    def get_margins(self, instrument, account_row, mmr, emr, lmr):
        """
        Checks whether the three level margin policy is used and specifies
        the three margin levels. Returns 'true' if margin policy is three 
        level and 'false' otherwise.

        Parameters:
            instrument : The name of the instrument to get the trading
                setting for.
            account_row : The account information for the account to
                get the trading setting for.
            mmr : [out] The maintenance margin level.
            emr	: [out] The entry margin level.
            lmr	: [out] The limitation margin level.
        
        Returns:
                
        """
        return self._b._getMargins(instrument, account_row, mmr, emr, lmr)

    def get_market_status(self, instrument):
        """
        Checks whether the trading in the instrument is allowed (whether
        the market is opened or closed).

        Parameters:
            instrument : The name of the instrument to get the trading
                setting for.
            
        Returns: string

        """
        return self._b._getMarketStatus(instrument)

    def get_max_quantity(self, instrument, account_row):
        """
        Gets the maximum size of a trade or of a market order.

        Parameters:
            instrument : The name of the instrument to get the trading
                setting for.
            account_row : The account information for the account to
                get the trading setting for.
            
        Returns: int

        """
        return self._b._getMaxQuantity(instrument, account_row)

    def get_max_trailing_step(self):
        """
        Gets the maximum size of the market movement after which an order
        must be moved following the market.
        
        Returns:

        """
        return self._b._getMaxTrailingStep()

    def get_min_quantity(self, instrument, account_row):
        """
        Gets the minimum size of a trade or of a market order.

        Parameters:
            instrument : The name of the instrument to get the trading
                setting for.
            account_row : The account information for the account to
                get the trading setting for.
            
        Returns:

        """
        return self._b._getMinQuantity(instrument, account_row)

    def get_min_trailing_step(self):
        """
        Gets the minimum size of the market movement after which an order
        must be moved following the market.
        
        Returns:        
                
        """
        return self._b._getMinTrailingStep()

    def get_mmr(self, instrument, account_row):
        """
        Gets the minimum margin requirement.

        Parameters:
            instrument : The name of the instrument to get the trading
                setting for.
            account_row : The account information for the account to
                get the trading setting for.
            
        Returns:

        """
        return self._b._getMMR(instrument, account_row)

