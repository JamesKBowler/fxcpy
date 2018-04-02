#pragma once

class ResponseListener : public IO2GResponseListener
{
    public:
        /** Request execution completed data handler. */
        virtual void onRequestCompleted(const char *requestId, IO2GResponse *response = 0) = 0;

        /** Request execution failed data handler. */
        virtual void onRequestFailed(const char *requestId , const char *error) = 0;

        /** Request update data received data handler. */
        virtual void onTablesUpdates(IO2GResponse *data) = 0;
        
};


//#pragma once
//
///** Response listener class. */
//class OrderMonitor;
//
//class ResponseListener : public IO2GResponseListener
//{
// public:
//    ResponseListener(IO2GSession *session);
//    virtual ~ResponseListener();
//    /** Increase reference counter. */
//    virtual long addRef();
//
//    /** Decrease reference counter. */
//    virtual long release();
//
//    /** Set request ID. */
//    void setRequestIDs(std::vector<std::string> &orderIDs);
//    void setRequestID(const char *sRequestID);
//
//    /** Wait for request execution or error. */
//    bool waitEvents();
//    void stopWaiting();
//
//    /** Get response.*/
//    IO2GResponse *getResponse();
//    
//    
//    bool hasError();
//    std::string getError();
//
//    /** Request execution completed data handler. */
//    virtual void onRequestCompleted(const char *requestId, IO2GResponse *response = 0);
//
//    /** Request execution failed data handler. */
//    virtual void onRequestFailed(const char *requestId , const char *error);
//
//    /** Request update data received data handler. */
//    virtual void onTablesUpdates(IO2GResponse *data);
//    
//    std::string getRequestID();
//
// private:
//    long mRefCount;
//    /** Session object. */
//    IO2GSession *mSession;
//    
//    IO2GLoginRules* mLoginRules;
//    /** Request we are waiting for. */
//    std::vector<std::string> mRequestIDs;
//    std::string mRequestID;
//    /** Response Event handle. */
//    HANDLE mResponseEvent;    
//    /** State of last request. */
//    IO2GResponse *mResponse;
//    /** State of last error. */
//    std::string mError;
//    bool mWasError;
//    
//    
//
//};
//
