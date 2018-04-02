#include "stdafx.h"
#include <IO2GResponse.h>
//#include <math.h>
//#include <boost/log/trivial.hpp>
//#include <sstream>
//#include <iomanip>
//#include "OrderMonitor.h"
//#include "ResponseListener.h"
//
//#if defined(_WIN32) || defined(WIN32)
//#define __PRETTY_FUNCTION__ __FUNCTION__
//#endif
//
//ResponseListener::ResponseListener(IO2GSession *session)
//{
//    mSession = session;
//    mSession->addRef();
//    mLoginRules = mSession->getLoginRules();
//    mRefCount = 1;
//    mResponseEvent = CreateEvent(0, FALSE, FALSE, 0);
//    mRequestID = "";
//    mResponse = NULL;
//    mError = "";
//    mWasError = false;
//    std::cout.precision(2);
//}
//
//ResponseListener::~ResponseListener()
//{
//    if (mResponse)
//        mResponse->release();
//    mSession->release();
//    CloseHandle(mResponseEvent);
//}
//
///** Increase reference counter. */
//long ResponseListener::addRef()
//{
//    //BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
//    return InterlockedIncrement(&mRefCount);
//}
//
///** Decrease reference counter. */
//long ResponseListener::release()
//{
//    //BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
//    long rc = InterlockedDecrement(&mRefCount);
//    if (rc == 0)
//        delete this;
//    return rc;
//}
//
///** Set multiple requests. */
//void ResponseListener::setRequestIDs(std::vector<std::string> &requestIDs)
//{
//    BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
//    mRequestIDs.resize(requestIDs.size());
//    std::copy(requestIDs.begin(), requestIDs.end(), mRequestIDs.begin());
//    ResetEvent(mResponseEvent);
//}
//
///** Set a single request. */
//void ResponseListener::setRequestID(const char *sRequestID)
//{
//    BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
//    mRequestID = sRequestID;
//    if (mResponse)
//    {
//        mResponse->release();
//        mResponse = NULL;
//    }
//    ResetEvent(mResponseEvent);
//}
//
///** Gets response.*/
//IO2GResponse *ResponseListener::getResponse()
//{
//    BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
//    if (mResponse)
//        //std::cout << "got response" << std::endl;
//        mResponse->addRef();
//    return mResponse;
//}
//
///** Gets error reason.*/
//std::string ResponseListener::getError()
//{
//    BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
//    return mError;
//}
//
//bool ResponseListener::hasError()
//{
//    BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
//    return mWasError;
//}
//
//bool ResponseListener::waitEvents()
//{
//    BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
//    return WaitForSingleObject(mResponseEvent, _TIMEOUT) == 0;
//}
//
//void ResponseListener::stopWaiting()
//{
//    BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
//    SetEvent(mResponseEvent);
//}
//
///** Request execution completed data handler. */
//void ResponseListener::onRequestCompleted(const char *requestId, IO2GResponse *response)
//{
//    BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
//    if (response && (mRequestID == requestId || std::find(
//        mRequestIDs.begin(), mRequestIDs.end(), requestId) != mRequestIDs.end()))
//    {
//        mResponse = response;
//        mResponse->addRef();
//        mWasError = false;
//        if (response->getType() != CreateOrderResponse)
//            stopWaiting();
//    }
//}
//
///** Request execution failed data handler. */
//void ResponseListener::onRequestFailed(const char *requestId , const char *error)
//{
//    BOOST_LOG_TRIVIAL(trace) << __PRETTY_FUNCTION__;
//    if (mRequestID == requestId || std::find(
//        mRequestIDs.begin(), mRequestIDs.end(), requestId) != mRequestIDs.end())
//    {
//        mError = error;
//        mWasError = true;
//        stopWaiting();
//    }
//}
//
///** Request update data received data handler. */
//void ResponseListener::onTablesUpdates(IO2GResponse *data)
//{
////    std::cout << "onTablesUpdates" << std::endl;
////    if (data)
////    {
////        O2G2Ptr<IO2GResponseReaderFactory> factory = mSession->getResponseReaderFactory();
////        if (factory)
////        {
////            O2G2Ptr<IO2GTablesUpdatesReader> reader = factory->createTablesUpdatesReader(data);
////            if (reader)
////            {
////                for (int i = 0; i < reader->size(); ++i)
////                {
////                    if (!mLoginRules->isTableLoadedByDefault(reader->getUpdateTable(i)))
////                    {
////                        switch (reader->getUpdateTable(i))
////                        {
////                            case Trades:
////                            std::cout << "onTablesUpdates::Trades" << std::endl;
////                            break;
////
////                            case Accounts:
////                            std::cout << "onTablesUpdates::Accounts" << std::endl;
////                            stopWaiting();
////                            break;
////
////                            case Offers:
////                            std::cout << "onTablesUpdates::Offers" << std::endl;
////                            break;
////
////                            case Orders:
////                            std::cout << "onTablesUpdates::Orders" << std::endl;
////                            break;
////
////                            case ClosedTrades:
////                            std::cout << "onTablesUpdates::ClosedTrades" << std::endl;
////                            break;
////                            
////                            case Messages:
////                            std::cout << "onTablesUpdates::Messages" << std::endl;
////                            break;
////                        }
////                    }    
////                }
////            }
////        }
////    }
//}
