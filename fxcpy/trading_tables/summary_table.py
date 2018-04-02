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
    IO2GSummaryRow,
    IO2GSummaryTable,
    O2GTable
)


class SummaryTable(object):
    def __init__(self, table_manager):
        self._table_manager = table_manager
        self._set_table()
    
    def _set_table(self):        
        self._table = self._table_manager.getTable(O2GTable.Summary)
        self._table.__class__ = IO2GSummaryTable
        
    def _find_row(self, offer_id):
        row = self._table.findRow(offer_id)
        if row:
            row.__class__ = IO2GSummaryRow
            row.release()
            return row

    def get_offer_id(self, offer_id):
        """
        The unique identification number of the instrument traded.

        Returns: string

        """
        summary_dict = {}
        for i in range(self._table.size()):
            row = self._table.getRow(i)
            if row:
                row.__class__ = IO2GSummaryRow
                summary_dict[row.getOfferID()] = row.getInstrument()
                row.release()
        return summary_dict

    def get_default_sort_order(self, offer_id):
        """
        The sequence number of the instrument. It defines the instrument 
        place in the dealing rates list of the FX Trading Station.

        Returns: integer

        """
        row = self._find_row(offer_id)
        if row:
            return row.getDefaultSortOrder()

    def get_instrument(self, offer_id):
        """
        The symbol of the instrument traded. For example, EUR/USD, USD/JPY, 
        GBP/USD.

        Returns: string

        """
        row = self._find_row(offer_id)
        if row:
            return row.getInstrument()

    def get_sell_net_pl(self, offer_id):
        """
        The current profit/loss of all short (sell) positions. It is expressed 
        in the account currency. It does not include commissions and interests.
        If no short positions exist for the instrument, the value of this field
        is 0.0.

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getSellNetPL()

    def get_sell_amount(self, offer_id):
        """
        The amount of short (sell) positions. In the case of FX instruments, 
        it is expressed in the instrument base currency. In the case of CFD 
        instruments, it is expressed in contracts. If short positions exist for
        the instrument traded, the value of this field is positive. Otherwise,
        the value of this field is 0.0.

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getSellAmount()

    def get_sell_avg_open(self, offer_id):
        """
        The average open price of short (sell) positions. In the case of FX 
        instruments, it is expressed in the instrument counter currency per one
        unit of base currency. In the case of CFD instruments, it is expressed 
        in the instrument native currency per one contract. If no short 
        positions exist for the instrument, the value of this field is 0.0.

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getSellAvgOpen()

    def get_buy_close(self, offer_id):
        """
        The current market price, at which short (sell) positions can be closed.
        In the case of FX instruments, it is expressed in the instrument counter
        currency per one unit of base currency. In the case of CFD instruments,
        it is expressed in the instrument native currency per one contract. If 
        no short positions exist for the instrument, the value of this 
        field is 0.0.

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getBuyClose()

    def get_sell_close(self, offer_id):
        """
        The current market price, at which long (buy) positions can be closed. 
        In the case of FX instruments, it is expressed in the instrument counter
        currency per one unit of base currency. In the case of CFD instruments,
        it is expressed in the instrument native currency per one contract. 
        If no long positions exist for the instrument, the value of this field 
        is 0.0.

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getSellClose()

    def get_buy_avg_open(self, offer_id):
        """
        The average open price of long (buy) positions. In the case of FX 
        instruments, it is expressed in the instrument counter currency per 
        one unit of base currency. In the case of CFD instruments, it is 
        expressed in the instrument native currency per one contract. If no 
        long positions exist for the instrument, the value of this field is 0.0.

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getBuyAvgOpen()

    def get_buy_amount(self, offer_id):
        """
        The amount of long (buy) positions. In the case of FX instruments, it 
        is expressed in the instrument base currency. In the case of CFD 
        instruments, it is expressed in contracts. If long positions exist for 
        the instrument traded, the value of this field is positive. Otherwise, 
        the value of this field is 0.0.

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getBuyAmount()

    def get_buy_net_pl(self, offer_id):
        """
        The current profit/loss of all long (buy) positions. It is expressed in 
        the account currency. It does not include commissions and interests. 
        If no long positions exist for the instrument, the value of this field 
        is 0.0.

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getBuyNetPL()

    def get_amount(self, offer_id):
        """
        The amount of all positions (both long and short). In the case of FX 
        instruments, it is expressed in the instrument base currency. In the 
        case of CFD instruments, it is expressed in contracts. If the amount of 
        long positions exceeds the amount of short positions for the instrument 
        traded, the value of this field is positive. If the amount of short 
        positions exceeds the amount of long positions for the instrument 
        traded, the value of this field is negative.

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getAmount()

    def get_gross_pl(self, offer_id):
        """
        The current profit/loss of all positions (both long and short). It is 
        expressed in the account currency. It does not include commissions and 
        interests.

        Returns: double

        """
        row = self._find_row(offer_id)
        if row:
            return row.getGrossPL()

    def get_net_pl(self, offer_id):
        """
        The current profit/loss of all positions (both long and short). It is 
        expressed in the account currency. It includes commissions and 
        interests.

        Returns: double
        
        """
        row = self._find_row(offer_id)
        if row:
            return row.getNetPL()