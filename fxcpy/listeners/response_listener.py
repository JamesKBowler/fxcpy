from forexconnect import ResponseListener as CResponseListener
from forexconnect import (
    ResponseUnknown,
    TablesUpdates,
    MarketDataSnapshot,
    GetAccounts,
    GetOffers,
    GetOrders,
    GetTrades,
    GetClosedTrades,
    GetMessages,
    CreateOrderResponse,
    GetSystemProperties,
    CommandResponse,
    MarginRequirementsResponse,
    GetLastOrderUpdate,
    MarketData
)

from forexconnect import (
    IO2GClosedTradeRow,
    IO2GTradeRow,
    IO2GOrderRow
)

from forexconnect import (
    Trades,
    Accounts,
    Offers,
    Orders,
    ClosedTrades,
    Messages
)

from eventfd import EventFD
from . import Counter

from ..logger import Log
log = Log().logger


class ResponseListener(CResponseListener):
    """
    The class provides method signatures to process notifications about request
    completions, request failures and tables updates.
    
    The interface must be implemented by an application in order to process the
    trading server responses.
    
    Responses come from the trading server in two ways:

    A response provided by the server as an answer to a user request.
    Requests may be successfully completed or failed:
    - to process notifications about successful requests completion,
      you must use the onRequestCompleted method;
    - to process notifications about requests failures,
      you must use the onRequestFailed method.

    A response provided by the server as a result of trading tables updates.
    To process these notifications, you must use the onTablesUpdates method.
  
    """
    def __init__(self, session):
        super().__init__()
        log.debug("")
        self._session = session
        self._session.addRef()
        self._init = {}
        self._init_completed = False
        self._refcount = Counter(1)
        self._event = EventFD()
        self._login_rules = session.getLoginRules()
        self._response = None
        self._error = None
        self._was_error = False

    def __del__(self):
        #log.debug("")
        if self._response:
            self._response.release()
        if self._session:
            self._session.release()
        self._event.clear()
        
    # CallBack from C++
    def addRef(self):
        """
        Called from the C++ code to add an object when 
        required.
        """
        self._refcount.increment()
        ref = self._refcount.value
        return ref
    
    # CallBack from C++
    def release(self):
        """
        Called from the C++ code to release an object when 
        finished.
        """
        self._refcount.decrement()
        ref = self._refcount.value
        if self._refcount.value == 0:
            del self
        return ref
    
    # CallBack from C++
    def _on_request_completed(self, request_id, response):
        """
        This method is called from the C++ code on a successfull
        command execution.
        
        It also releases to GIL after logging in, by calling stop_waiting()
        
        """
        response_type = response.getType()
        if self._init_completed:
            self._response = response
            self._response.addRef()
            self._was_error = False
            
            if response_type == ResponseUnknown:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == TablesUpdates:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == MarketDataSnapshot:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == GetAccounts:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == GetOffers:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == GetOrders:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == GetTrades:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == GetClosedTrades:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == GetMessages:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == CreateOrderResponse:
                #self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == GetSystemProperties:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == CommandResponse:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == MarginRequirementsResponse:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == GetLastOrderUpdate:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            elif response_type == MarketData:
                self.stop_waiting()
                log.debug("{} {}".format(response_type.name, request_id))
                
            else:
                log.error("ResponseType not found {} {}".format(
                    response_type.name, request_id)
                )
        else:
            if request_id[-1] in ['4','6','7','8']:
                factory = self._session.getResponseReaderFactory()
                if factory:
                    if request_id[-1] == '4' and response_type == GetOrders:
                        log.debug("Initial {} {}".format(
                            response_type.name, request_id)
                        )
                        reader = factory.createOrdersTableReader(response)
                        if reader:
                            self._init['orders'] = []
                            for i in range(reader.size()):
                                row = reader.getRow(i)
                                row.__class__ = IO2GOrderRow
                                self._init['orders'].append(row)

                    elif request_id[-1] == '7' and response_type == GetClosedTrades:
                        log.debug("Initial {} {}".format(
                            response_type.name, request_id)
                        )
                        reader = factory.createClosedTradesTableReader(response)
                        if reader:
                            self._init['closed_trades'] = []
                            for i in range(reader.size()):
                                row = reader.getRow(i)
                                row.__class__ = IO2GClosedTradeRow
                                self._init['closed_trades'].append(row)
                                
                    elif request_id[-1] == '6' and response_type == GetTrades:
                        log.debug("Initial {} {}".format(
                            response_type.name, request_id)
                        )
                        reader = factory.createTradesTableReader(response)
                        if reader:
                            self._init['trades'] = []
                            for i in range(reader.size()):
                                row = reader.getRow(i)
                                row.__class__ = IO2GTradeRow
                                self._init['trades'].append(row)

                    elif request_id[-1] == '8' and response_type == CommandResponse:
                        log.debug("Initial {} {}".format(
                            response_type.name, request_id)
                        )
                        self._init_completed = True
                        self.stop_waiting()
            
    # CallBack from C++
    def _on_request_failed(self, request_id , error):
        """
        Request failed execution data handler.
        """
        log.error("Request {} : Reason {}".format(request_id, error))
        self._error = error
        self._was_error = True
        self.stop_waiting()
    
    # CallBack from C++
    def _on_tables_updates(self, data):
        """
        Represents table updates response that are provided by the trading
        server automatically.
        
        Currently this method is not implementing anything, it is merely here
        to provide a starting point.
        
        C++ exmaple of this method can be found in the C++ API downloads
        section:        
        http://http://fxcodebase.com/wiki/index.php/Category:ForexConnect

        """
        if data:
            factory = self._session.getResponseReaderFactory()
            if factory:
                reader = factory.createTablesUpdatesReader(data)
                if reader:
                    for i in range(reader.size()):
                        # Only implement if table manger is not loaded on login session
                        update = reader.getUpdateTable(i)
                        if update == Trades:
                            pass  #log.debug("Trades")

                        elif update == Accounts:
                            pass  #log.debug("Accounts")

                        elif update == Offers:
                            pass  #log.debug("Offers")

                        elif update == Orders:
                            pass  #log.debug("Orders")

                        elif update == ClosedTrades:
                            pass  #log.debug("ClosedTrades")

                        elif update == Messages:
                            pass  #log.debug("Messages")

                        else:
                            pass  #log.error("UpdateType not found!")
                else:
                    log.error("reader not found!")    
                    
            else:
                log.error("factory not found!")

    def clear_last_responce(self):
        if self._response:
            self._response.release()
        self._response = None
            
    def get_response(self):
        """
        Get the last response retrived from the trading server
        """
        log.debug("")
        if self._response:
            self._response.addRef()
        return self._response

    def get_error(self):
        """
        Get the last error retrived from the trading server
        """
        error = self._error
        self._error = None
        self._was_error = False
        return error

    def has_error(self):
        """
        Bool true or false
        """
        return self._was_error

    def wait_events(self):
        """
        Locks the GIL.
        """
        log.debug("")
        try: return self._event.wait(timeout=10)
        finally: self._event.clear()

    def stop_waiting(self):
        """
        Unlocks the GIL.
        """
        log.debug("")
        self._event.set()