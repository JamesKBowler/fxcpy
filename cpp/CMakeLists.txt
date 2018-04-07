cmake_minimum_required(VERSION 3.9)
#set(Boost_DEBUG ON)
set(ROOT ${CMAKE_SOURCE_DIR})
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")
find_package(Boost 1.6 COMPONENTS python3 REQUIRED)
find_package(PythonLibs 3 REQUIRED)
find_package(ForexConnectAPI REQUIRED)
add_definitions(-DBOOST_LOG_DYN_LINK)
message(STATUS ${FOREXCONNECT_LIBRARIES})
#set(BOOST_ROOT "/usr/local/include" )
#set(BOOST_INCLUDEDIR "/usr/local/include/boost/")
#set(BOOST_LIBRARYDIR "/usr/local/include/boost")

include_directories(
  ${Boost_INCLUDE_DIRS}
  ${PYTHON_INCLUDE_DIR}
  ${FOREXCONNECT_INCLUDE_DIR})

execute_process (
  COMMAND python3 -c "import site; print(site.getsitepackages()[0])"
  OUTPUT_VARIABLE INSTALL_PYTHON_PKG_DIR OUTPUT_STRIP_TRAILING_WHITESPACE)

set(INSTALL_TARGETS_DEFAULT_ARGS
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib)

include_directories(src ${CMAKE_CURRENT_BINARY_DIR}/src)

set(SRCS src/forexconnect.cpp
    src/IAddRef.cpp
    src/IO2GRow.cpp
    src/IO2GColumn.cpp
    src/IO2GTable.cpp

    src/IO2GRequest.cpp
    src/IO2GResponse.cpp
    src/IO2GSession.cpp
    src/O2GTransport.cpp

    src/IO2GLoginRules.cpp
    src/IO2GPermissionChecker.cpp
    src/IO2GTradingSettingsProvider.cpp

    src/IO2GTimeframe.cpp
    src/IO2GTimeConverter.cpp
    src/O2GDateUtils.cpp

    src/O2G2ptr.cpp
    src/O2GEnum.cpp
    src/O2GRequestParamsEnum.cpp

    src/Rows/IO2GClosedTradeRow.cpp
    src/Rows/IO2GMessageRow.cpp
    src/Rows/IO2GOfferRow.cpp
    src/Rows/IO2GOrderRow.cpp
    src/Rows/IO2GSummaryRow.cpp
    src/Rows/IO2GTradeRow.cpp
    src/Rows/IO2GAccountRow.cpp

    src/Enums/ClosedTradesColumnsEnum.cpp
    src/Enums/AccountsColumnsEnum.cpp
    src/Enums/OffersColumnsEnum.cpp
    src/Enums/OrdersColumnsEnum.cpp
    src/Enums/SummariesColumnsEnum.cpp
    src/Enums/TradesColumnsEnum.cpp
    src/Enums/MessagesColumnsEnum.cpp

    src/Readers/IO2GTablesUpdatesReader.cpp    
    src/Readers/IO2GMarketDataResponseReader.cpp
    src/Readers/IO2GMarketDataSnapshotResponseReader.cpp
    src/Readers/IO2GLastOrderUpdateResponseReader.cpp
    src/Readers/IO2GOrderResponseReader.cpp
    src/Readers/IO2GSystemPropertiesReader.cpp
)

add_library(forexconnect SHARED ${SRCS})

target_link_libraries(forexconnect
  ${FOREXCONNECT_LIBRARIES}
  ${Boost_LIBRARIES}
  ${PYTHON_LIBLARY})

set_target_properties(forexconnect PROPERTIES PREFIX "")

install(TARGETS forexconnect
	ARCHIVE DESTINATION ${INSTALL_PYTHON_PKG_DIR}
	LIBRARY DESTINATION ${INSTALL_PYTHON_PKG_DIR})
