#include "stdafx.h"
#include <IO2GTradingSettingsProvider.h>
using namespace boost::python;

//IO2GTradingSettingsProvider
class IO2GTradingSettingsProviderWrap : public IO2GTradingSettingsProvider, public wrapper<IO2GTradingSettingsProvider>
{
public:
	int getCondDistStopForTrade(const char* instrument){ return this->get_override("_getCondDistStopForTrade")();}
	int getCondDistLimitForTrade(const char* instrument){ return this->get_override("_getCondDistLimitForTrade")();}
	int getCondDistEntryStop(const char* instrument){ return this->get_override("_getCondDistEntryStop")();}
	int getCondDistEntryLimit(const char* instrument){ return this->get_override("_getCondDistEntryLimit")();}
	int getMinQuantity(const char* instrument, IO2GAccountRow* account){ return this->get_override("_getMinQuantity")();}
	int getMaxQuantity(const char* instrument, IO2GAccountRow* account){ return this->get_override("_getMaxQuantity")();}
	int getBaseUnitSize(const char* instrument, IO2GAccountRow* account){ return this->get_override("_getBaseUnitSize")();}
	O2GMarketStatus getMarketStatus(const char* instrument){ return this->get_override("_getMarketStatus")();}
	int getMinTrailingStep(){ return this->get_override("_getMinTrailingStep")();}
	int getMaxTrailingStep(){ return this->get_override("_getMaxTrailingStep")();}
	double getMMR(const char* instrument, IO2GAccountRow* account){ return this->get_override("_getMMR")();}
	bool getMargins(const char* instrument, IO2GAccountRow* account, double& mmr, double& emr, double& lmr)
	{ return this->get_override("_getMargins")();}
};

void export_IO2GTradingSettingsProvider()
{
	class_<IO2GTradingSettingsProviderWrap, bases<IAddRef>, boost::noncopyable>("IO2GTradingSettingsProvider", no_init)
		.def("_getCondDistStopForTrade", pure_virtual(&IO2GTradingSettingsProvider::getCondDistStopForTrade))
		.def("_getCondDistLimitForTrade", pure_virtual(&IO2GTradingSettingsProvider::getCondDistLimitForTrade))
		.def("_getCondDistEntryStop", pure_virtual(&IO2GTradingSettingsProvider::getCondDistEntryStop))
		.def("_getCondDistEntryLimit", pure_virtual(&IO2GTradingSettingsProvider::getCondDistEntryLimit))
		.def("_getMinQuantity", pure_virtual(&IO2GTradingSettingsProvider::getMinQuantity))
		.def("_getMaxQuantity", pure_virtual(&IO2GTradingSettingsProvider::getMaxQuantity))
		.def("_getBaseUnitSize", pure_virtual(&IO2GTradingSettingsProvider::getBaseUnitSize))
		.def("_getMarketStatus", pure_virtual(&IO2GTradingSettingsProvider::getMarketStatus))
		.def("_getMinTrailingStep", pure_virtual(&IO2GTradingSettingsProvider::getMinTrailingStep))
		.def("_getMaxTrailingStep", pure_virtual(&IO2GTradingSettingsProvider::getMaxTrailingStep))
		.def("_getMMR", pure_virtual(&IO2GTradingSettingsProvider::getMMR))
		.def("_getMargins", pure_virtual(&IO2GTradingSettingsProvider::getMargins))
		;
};