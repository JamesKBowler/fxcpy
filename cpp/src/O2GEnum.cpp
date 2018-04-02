#include "stdafx.h"
#include <O2GEnum.h>

void export_O2GEnum()
{
    using namespace boost::python;
// error
	enum_<O2GTable>("O2GTable")
		.value("TableUnknown", TableUnknown)
		.value("Offers", Offers)
		.value("Accounts", Accounts)
		.value("Orders", Orders)
		.value("Trades", Trades)
		.value("ClosedTrades", ClosedTrades)
		.value("Messages", Messages)
		.value("Summary", Summary)
		.export_values()
		;

	enum_<O2GResponseType>("O2GResponseType")
		.value("ResponseUnknown", ResponseUnknown)
		.value("TablesUpdates", TablesUpdates)
		.value("MarketDataSnapshot", MarketDataSnapshot)
		.value("GetAccounts", GetAccounts)
		.value("GetOffers", GetOffers)
		.value("GetOrders", GetOrders)
		.value("GetTrades", GetTrades)
		.value("GetClosedTrades", GetClosedTrades)
		.value("GetMessages", GetMessages)
		.value("CreateOrderResponse", CreateOrderResponse)
		.value("GetSystemProperties", GetSystemProperties)
		.value("CommandResponse", CommandResponse)
		.value("MarginRequirementsResponse", MarginRequirementsResponse)
		.value("GetLastOrderUpdate", GetLastOrderUpdate)
		.value("MarketData", MarketData)
		.export_values()
		;

	enum_<O2GTableUpdateType>("O2GTableUpdateType")
		.value("UpdateUnknown", UpdateUnknown)
		.value("Insert", Insert)
		.value("Update", Update)
		.value("Delete", Delete)
		.export_values()
		;

	enum_<O2GPermissionStatus>("O2GPermissionStatus")
		.value("PermissionDisabled", PermissionDisabled)
		.value("PermissionEnabled", PermissionEnabled)
		.value("PermissionHidden ", PermissionHidden)
		.export_values()
		;

	enum_<O2GMarketStatus>("O2GMarketStatus")
		.value("MarketStatusOpen", MarketStatusOpen)
		.value("MarketStatusClosed", MarketStatusClosed)
		.value("MarketStatusUndefined", MarketStatusUndefined)
		.export_values()
		;

	enum_<O2GPriceUpdateMode>("O2GPriceUpdateMode")
		.value("Default", Default)
		.value("NoPrice", NoPrice)
		.export_values()
		;

	enum_<O2GTableManagerMode>("O2GTableManagerMode")
		.value("No", No)
		.value("Yes", Yes)
		.export_values()
		;

	enum_<O2GTableStatus>("O2GTableStatus")
		.value("Initial", Initial)
		.value("Refreshing", Refreshing)
		.value("Refreshed", Refreshed)
		.value("Failed", Failed)
		.export_values()
		;
        
// Not supported anymore
//	enum_<O2GReportUrlError>("O2GReportUrlError")
//		.value("ReportUrlNotSupported", O2GReportUrlError::ReportUrlNotSupported)
//		.value("ReportUrlTooSmallBuffer", O2GReportUrlError::ReportUrlTooSmallBuffer)
//		.value("ReportUrlNotLogged", O2GReportUrlError::ReportUrlNotLogged)
//		.export_values()
//		;

	enum_<O2GTableManagerStatus>("O2GTableManagerStatus")
		.value("TablesLoading", TablesLoading)
		.value("TablesLoaded", TablesLoaded)
		.value("TablesLoadFailed", TablesLoadFailed)
		.export_values()
		;
        
	enum_<O2GCandleOpenPriceMode>("O2GCandleOpenPriceMode")
		.value("PreviousClose", PreviousClose)
		.value("FirstTick", FirstTick)
		.export_values()
		;
        
}