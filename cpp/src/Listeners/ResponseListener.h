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