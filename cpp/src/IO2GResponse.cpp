#include "stdafx.h"
#include "IO2GResponse.h"
#include "Listeners/ResponseListener.h"
#include <boost/log/trivial.hpp>

#if defined(_WIN32) || defined(WIN32)
#define __PRETTY_FUNCTION__ __FUNCTION__
#endif


using namespace boost::python;

class IO2GResponseWrap : public IO2GResponse, public wrapper < IO2GResponse >
{
public:
	O2GResponseType getType() { return this->get_override("getType")(); }
	const char * getRequestID() { return this->get_override("getRequestID")(); }
};

class IO2GResponseListenerWrap : public IO2GResponseListener, public wrapper < IO2GResponseListener >
{
public:
	void onRequestCompleted(const char * requestId, IO2GResponse* response) { this->get_override("_on_request_completed")(); }
	void onRequestFailed(const char * requestId, const char * error) { this->get_override("_on_request_failed")(); }
	void onTablesUpdates(IO2GResponse * data) { this->get_override("_on_tables_updates")(); }
};


class IO2GResponseReaderFactoryWrap : public IO2GResponseReaderFactory, public wrapper < IO2GResponseReaderFactory >
{
public:
	IO2GTablesUpdatesReader* createTablesUpdatesReader(IO2GResponse *response){ return this->get_override("createTablesUpdatesReader")(); }
	IO2GMarketDataSnapshotResponseReader* createMarketDataSnapshotReader(IO2GResponse *response){ return this->get_override("createMarketDataSnapshotReader")(); }
	IO2GMarketDataResponseReader* createMarketDataReader(IO2GResponse *response){ return this->get_override("createMarketDataReader")(); }
	IO2GOffersTableResponseReader* createOffersTableReader(IO2GResponse *response){ return this->get_override("createOffersTableReader")(); }
	IO2GAccountsTableResponseReader* createAccountsTableReader(IO2GResponse *response){ return this->get_override("createAccountsTableReader")(); }
	IO2GOrdersTableResponseReader* createOrdersTableReader(IO2GResponse *response){ return this->get_override("createOrdersTableReader")(); }
	IO2GTradesTableResponseReader* createTradesTableReader(IO2GResponse *response){ return this->get_override("createTradesTableReader")(); }
	IO2GClosedTradesTableResponseReader* createClosedTradesTableReader(IO2GResponse *response){ return this->get_override("createClosedTradesTableReader")(); }
	IO2GMessagesTableResponseReader* createMessagesTableReader(IO2GResponse *response){ return this->get_override("createMessagesTableReader")(); }
	IO2GOrderResponseReader* createOrderResponseReader(IO2GResponse *response){ return this->get_override("createOrderResponseReader")(); }
	IO2GLastOrderUpdateResponseReader* createLastOrderUpdateResponseReader(IO2GResponse *response){ return this->get_override("createLastOrderUpdateResponseReader")(); }
	IO2GSystemPropertiesReader* createSystemPropertiesReader(IO2GResponse *response){ return this->get_override("createSystemPropertiesReader")(); }
	bool processMarginRequirementsResponse(IO2GResponse *response){ return this->get_override("processMarginRequirementsResponse")(); }
};


class gil_lock
{
public:
        gil_lock()
        {
            state_ = PyGILState_Ensure();
        }
        ~gil_lock()
        {
            PyGILState_Release(state_);
        }
private:
        PyGILState_STATE state_;
};

class ResponseListenerCallback : public ResponseListener
{
public:
	ResponseListenerCallback(PyObject *pyObject)
		: self(pyObject) {}

	ResponseListenerCallback(PyObject* pyObject, const ResponseListener& listener)
		: self(pyObject), ResponseListener(listener) {}

	void onRequestCompleted(const char *requestId, IO2GResponse *response)
	{
                //BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
                gil_lock lock;
                try
                {
                        call_method<void>(self, "_on_request_completed", requestId, boost::ref(response));
                }
                catch(error_already_set)
                {
                        PyErr_Print();
                }
	}
	
	void onRequestFailed(const char *requestId , const char *error)
	{
                //BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
                gil_lock lock;
                try
                {
                        call_method<void>(self, "_on_request_failed", requestId, error);                
                }
                catch(error_already_set)
                {
                        PyErr_Print();
                }
	}
        
	void onTablesUpdates(IO2GResponse *data)
	{
                //BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
                gil_lock lock;
                try
                {
                    call_method<void>(self, "_on_tables_updates", boost::ref(data));                
                }
                catch(error_already_set)
                {
                    PyErr_Print();
                }
	}
        
	long addRef()
	{
                //BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
                gil_lock lock;
                try
                {
                        return call_method<long>(self, "addRef");
                }
                catch(error_already_set)
                {
                        PyErr_Print();
                }
	}

	long release()
	{
                //BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
                gil_lock lock;
                try
                {
                        return call_method<long>(self, "release");
                }
                catch(error_already_set)
                {
                        PyErr_Print();
                }
	}

private:
	PyObject* const self;
};


void export_IO2GResponse()
{
	class_<IO2GResponseListenerWrap, bases<IAddRef>, boost::noncopyable>("IO2GResponseListener", no_init)
		.def("_on_request_completed", pure_virtual(&IO2GResponseListener::onRequestCompleted)) 
		.def("_on_request_failed", pure_virtual(&IO2GResponseListener::onRequestFailed))
		.def("_on_tables_updates", pure_virtual(&IO2GResponseListener::onTablesUpdates))
		;
        
	class_<IO2GResponseReaderFactoryWrap, bases<IAddRef>, boost::noncopyable >("IO2GResponseReaderFactory", no_init)
		.def("createTablesUpdatesReader", pure_virtual(&IO2GResponseReaderFactory::createTablesUpdatesReader), return_value_policy<reference_existing_object>())
		.def("createMarketDataSnapshotReader", pure_virtual(&IO2GResponseReaderFactory::createMarketDataSnapshotReader), return_value_policy<reference_existing_object>())
		.def("createMarketDataReader", pure_virtual(&IO2GResponseReaderFactory::createMarketDataReader), return_value_policy<reference_existing_object>())
		.def("createOffersTableReader", pure_virtual(&IO2GResponseReaderFactory::createOffersTableReader), return_value_policy<reference_existing_object>())
		.def("createAccountsTableReader", pure_virtual(&IO2GResponseReaderFactory::createAccountsTableReader), return_value_policy<reference_existing_object>())
		.def("createOrdersTableReader", pure_virtual(&IO2GResponseReaderFactory::createOrdersTableReader), return_value_policy<reference_existing_object>())
		.def("createTradesTableReader", pure_virtual(&IO2GResponseReaderFactory::createTradesTableReader), return_value_policy<reference_existing_object>())
		.def("createClosedTradesTableReader", pure_virtual(&IO2GResponseReaderFactory::createClosedTradesTableReader), return_value_policy<reference_existing_object>())
		.def("createMessagesTableReader", pure_virtual(&IO2GResponseReaderFactory::createMessagesTableReader), return_value_policy<reference_existing_object>())
		.def("createOrderResponseReader", pure_virtual(&IO2GResponseReaderFactory::createOrderResponseReader), return_value_policy<reference_existing_object>())
		.def("createLastOrderUpdateResponseReader", pure_virtual(&IO2GResponseReaderFactory::createLastOrderUpdateResponseReader), return_value_policy<reference_existing_object>())
		.def("createSystemPropertiesReader", pure_virtual(&IO2GResponseReaderFactory::createSystemPropertiesReader), return_value_policy<reference_existing_object>())
		.def("processMarginRequirementsResponse", pure_virtual(&IO2GResponseReaderFactory::processMarginRequirementsResponse))
		;

	class_<ResponseListener, ResponseListenerCallback, bases<IO2GResponseListener>, boost::noncopyable >("ResponseListener", init<>())
		.def("_on_request_completed", &ResponseListenerCallback::onRequestCompleted)
		.def("_on_request_failed", &ResponseListenerCallback::onRequestFailed)
		.def("_on_tables_updates", &ResponseListenerCallback::onTablesUpdates)
		.def("addRef", &ResponseListenerCallback::addRef)
		.def("release", &ResponseListenerCallback::release)
		;
        
	class_<IO2GResponseWrap, bases<IAddRef>, boost::noncopyable>("IO2GResponse", no_init)
		.def("getType", pure_virtual(&IO2GResponse::getType))
		.def("getRequestID", pure_virtual(&IO2GResponse::getRequestID))
		;
};