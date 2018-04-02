from ..exception import RequestTimeOutError

from forexconnect import (
    MarketDataSnapshot,
    O2GCandleOpenPriceMode
)

from ..utils.date_utils import fm_ole

import numpy as np


class MarketData(object):
    """
    The MarketData class is designed to...
    
    TODO...
    """
    def __init__(
        self, session, response_listener,
        response_reader_factory, request_factory
    ):        
        """
        TODO...
        """
        self.session = session
        self.response_listener = response_listener
        self.response_reader_factory = response_reader_factory
        self.request_factory = request_factory

    def dtype(self):
        """
        TODO...
        """
        return np.dtype(
            [('date', 'datetime64[s]'), ('askopen', '<f8'),
             ('askhigh', '<f8'), ('asklow', '<f8'),
             ('askclose', '<f8'), ('bidopen', '<f8'),
             ('bidhigh', '<f8'), ('bidlow', '<f8'),
             ('bidclose', '<f8'), ('volume', '<i8')]
        )

    def get_price_data(
        self, instrument, timeframe, dtFrom, dtTo, incWeekendData=False,
        PriceMode=O2GCandleOpenPriceMode.PreviousClose
    ):  
        """
        Params : str "GBP/USD", str "D1", float 0.0, float 0.0
        
        Optional :
            > bool for weekend data
            > PreviousClose or FirstTick
            
        Returns : Structured Numpy Array
        np.array([
            ('2018-02-22T22:00:00', 1.39587, 1.40062, 1.39044, 1.3977 , 1.39506, 1.4005 , 1.39043, 1.39689, 315585),
            ('2018-02-25T22:00:00', 1.3991 , 1.40706, 1.39288, 1.39702, 1.3985 , 1.40695, 1.39275, 1.39651, 306833),
            ('2018-02-26T22:00:00', 1.39702, 1.39974, 1.38583, 1.39124, 1.39651, 1.39958, 1.3857 , 1.3904 , 393485),
            ('2018-02-27T22:00:00', 1.39124, 1.39169, 1.37571, 1.37629, 1.3904 , 1.39157, 1.37562, 1.3759 , 377407),
            ('2018-02-28T22:00:00', 1.37629, 1.37863, 1.37123, 1.37783, 1.3759 , 1.37848, 1.37111, 1.37745, 300786),
            ('2018-03-01T22:00:00', 1.37783, 1.38177, 1.37562, 1.38046, 1.37745, 1.38162, 1.37548, 1.37992, 289091),
            ('2018-03-04T22:00:00', 1.38026, 1.38783, 1.37674, 1.38503, 1.37984, 1.38769, 1.37658, 1.38478, 319845),
            ('2018-03-05T22:00:00', 1.38503, 1.39304, 1.38175, 1.3889 , 1.38478, 1.39289, 1.3816 , 1.38848, 305963),
            ('2018-03-06T22:00:00', 1.3889 , 1.39135, 1.38469, 1.3902 , 1.38848, 1.39121, 1.38453, 1.38943, 326001),
            ('2018-03-07T22:00:00', 1.3902 , 1.39111, 1.37824, 1.38121, 1.38943, 1.39093, 1.37803, 1.38061, 672878),
            ('2018-03-08T22:00:00', 1.38121, 1.389  , 1.3789 , 1.38549, 1.38061, 1.38886, 1.37875, 1.38486, 309030)],
            dtype=[('date', '<M8[s]'), ('askopen', '<f8'), ('askhigh', '<f8'), ('asklow', '<f8'), ('askclose', '<f8'),
                  ('bidopen', '<f8'), ('bidhigh', '<f8'), ('bidlow', '<f8'), ('bidclose', '<f8'), ('volume', '<i8')]
        )
        """
        # Date param check
        if not isinstance(dtFrom, float) or not isinstance(dtTo, float):
            raise AttributeError(
                "Dates must be float (OLE Automation)"
            )
        # Timeframe param check
        timeframeCollection = self.request_factory.getTimeFrameCollection()
        _timeframe = timeframeCollection.get(timeframe)
        if _timeframe is None:
            raise AttributeError(
                "Time frame {} not supported".format(timeframe)
            )
        # Create MarketDataSnapshot request
        request = self.request_factory.createMarketDataSnapshotRequestInstrument(
            instrument, _timeframe, _timeframe.getQueryDepth())
        if request is None:
            raise NameError(
                "Request not found, check request_factory or instrument spelling"
            )
        
        dtFirst = dtTo
        while dtFirst - dtFrom > 0.0001:
            # Request data range
            self.request_factory.fillMarketDataSnapshotRequestTime(
                request, dtFrom, dtFirst, incWeekendData, PriceMode
            )
            self.session.sendRequest(request)
            # Catch timeout errors
            if not self.response_listener.wait_events():
                raise RequestTimeOutError("waitEvents() timeout error")
            
            else:
                # Grap response and create reader
                response = self.response_listener.get_response()
                if (response and response.getType() == MarketDataSnapshot):
                    reader = self.response_reader_factory.createMarketDataSnapshotReader(response)
                    if reader:
                        if (abs(dtFirst - reader.getDate(0)) > 0.0001):
                            # Switch to earlest date
                            dtFirst = reader.getDate(0)
                        else:
                            break
                    else:
                        break
                    # Extract data from response
                    rows = []
                    for ii in range(reader.size()):
                        dt = reader.getDate(ii);
                        if reader.isBar():
                            rows.append((fm_ole(dt),
                                reader.getAskOpen(ii),
                                reader.getAskHigh(ii),
                                reader.getAskLow(ii),
                                reader.getAskClose(ii),
                                reader.getBidOpen(ii),
                                reader.getBidHigh(ii),
                                reader.getBidLow(ii),
                                reader.getBidClose(ii),
                                reader.getVolume(ii))
                            )
                        else:  # isTick()
                            rows.append((fm_ole(dt),
                                reader.getAsk(ii),
                                reader.getBid(ii))
                            )
                    # Structured numpy array
                    yield np.array(rows, dtype=self.dtype())
                else:
                    break