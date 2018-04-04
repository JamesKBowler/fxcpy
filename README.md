# fxcpy
fxcpy is an open-soured python implementation of the Forexconnect API SDK offered by FXCM. The full documentation can be found **[here](http://fxcodebase.com/bin/forexconnect/1.4.1/help/CPlusPlus/web-content.html#index.html)**

# Current Features
* **Trading Tables** - fxcpy supports all trading tables in memory for fast access updated automatically by the trading server.
    * `AccountsTable` -  contains the data such as account balance, used margin, daily PnL, Gross PnL etc...
    * `OffersTable` - all instrument attributes, such as symbol, live bid/ask pricing, point-size, contract currency etc ...
    * `OrdersTable` - holds order attributes until the are executed.
    * `TradesTable` - once orders are executed, trades are inserted and tracked with various attributes.
    * `ClosedTradesTable` - contains trades that are closed for the current trading day.
    * `SummaryTable` - contains summarised information for every instrument with an open position. 
    * `MessagesTable` - deals with messages sent from the trading server, such margin call.

* **Trading** - fxcpy is very flexible with many options for executing different types of orders.
    * OCO (One-Cancels-Other)
    * OTO (One-Triggers-Others)
    * OTOCO (One-Triggers-OCO)
    * Limit, Entry Limit, Trailing Entry Limit
    * Open/Close Market, Market Range
    * Open/Close Limit, Limit Range
    * Stop, Entry Stop, Trailing Stop
    * NET Orders
    * Order cloning 

* **Data** - fxcpy supports both live streaming and historical price data

## Requirements  
- Ubuntu 16.04
- boost 1.65.1  
- cmake 3.9.6  
- ForexConnectAPI 1.4.1 (included)

### Installation  
A large part of installing this API has to do with Boost & CMAKE, therefore the `install_script.sh` includes the installation of both and this API. Currently, Ubuntu 16.04 is supported, there are no plans to support the Windows operating system. However, support will be added for other Linux variants shortly.

Please become familiar with the installation process and remove any elements already installed on your system. If boost 1.65.1 or higher is installed using a different path than the usual `/usr:/usr/local...etc`, edit the commented values in the CMakeLists.txt file located in the `/cpp` directory.

First download this repository.

```shell    
git clone https://github.com/JamesKBowler/fxcpy.git
```

Switch to the `fxcpy/` directory.

```shell
cd fxcpy/
```

Once happy with the script execute following.

```shell
chmod +x install_script.sh && sudo ./install_script.sh
```

The script will add an environment variable to /etc/environment file. However, this will not come into effect until your machine is either rebooted or logged out and back in.

To find out more about environment variables, please read **[this](https://askubuntu.com/questions/866161/setting-path-variable-in-etc-environment-vs-profile?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)** question on askubuntu.

```shell
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/fxcpy/cpp/lib
```

After installation your system will have two modules `forexconnect` and `fxcpy`. Oh and `pandas` if not already installed.

The `forexconnect` module is a C++ Wrapper and `fxcpy` is the python implementation. Before using this API in a live trading environment, I **highly recommend** testing it first on a demo account, opened for free at https://www.fxcm.com/uk/forex-trading-demo/ 

Having FXCM's **[Trading Station](https://www.fxcm.com/uk/platforms/trading-station/download/)** open at the same to see trades simultaneously executed is a good idea.

### Basic Usage

We won't discuss best practices for storing passwords and for simplicity, create a setting.py file to hold your FXCM user, password, environment and url information.

An example of such is.

```python
# /fxcpy/fxcpy/settings.py

USER = "DEM12345"
PASS = "123456"
URL = "http://www.fxcorporate.com/Hosts.jsp"
ENV = "demo"  # or "real"
```

To get started create a session by logging into your FXCM account

```python
from fxcpy.session_handler import SessionHandler
from fxcpy.settings import USER, PASS, URL, ENV

session_handler = SessionHandler(USER, PASS, URL, ENV, load_tables=True)
```

Monitoring session status is carried out through the `SessionMonitoring` class,  located within the `SessionHandler`

```python
status = session_handler.session_monitoring.get_status()
```

To obtain information for all offers at FXCM, get the `OffersTable` class from the `SessionHandler`

```python
offers_table = session_handler.get_offers_table()
```

The Forexconnect API has no built-in function to find attributes using the instrument symbol, so we must always pass the unique `offer_id`. Sure, one could build such a feature. However, this would involve looping over each row in the table on every call.
    
All offer attributes are accessed through the `OffersTable` like this.

```python
offer = offers_table.get_offer_ids()

offer = {
    'AUD/CAD': '16',
    'AUD/CHF': '39',
    'AUD/JPY': '17',
    'AUD/NZD': '28',
    'AUD/USD': '6',
    'AUS200': '1001',
    'Bund': '3001',
    'CAD/CHF': '90',
    'CAD/JPY': '18',
    'CHF/JPY': '12',
    'CHN50': '1020',
    'Copper': '1016',
    'ESP35': '1002',
    'EUR/AUD': '14',
    'EUR/USD': '1',
    .....
}

offers_table.get_contract_currency(offer['EUR/USD'])
```

All other tables such as are accessed the same way.

```python
orders_table.get_whatever(order_id)
trades_table.get_whatever(trade_id)
```

and so on ..

Executing a trade is super easy using the`TradingCommands` class.

```python
trading_commands = session_handler.get_trading_commands()
```

Next, execute 5 SHORT trades for the EUR/USD, with stop loss and limit orders.

This example will place a stop loss 15 pips above and a limit order 30 pips below the current price.

```python
# Setup order to execute at market with stop and limit order
offer_id = "1" # EUR/USD
# Master valuemap container
master_valuemap = trading_commands.create_valuemap()
for i in range(5):
    # Create the order
    child_valuemap = trading_commands.create_open_market_order(offer_id, "S", 1)
    master_valuemap.appendChild(child_valuemap)
    # 15 pip stop
    rate_stop = offers_table.get_bid(offer_id) + 15.0 * offers_table.get_point_size(offer_id)
    # 30 pip profit
    rate_limit = offers_table.get_bid(offer_id) - 30.0 * offers_table.get_point_size(offer_id)
    # Attach
    master_valuemap = trading_commands.attach_stoplimit_orders(
            i, # valuemap index
            master_valuemap,
            rate_stop=rate_stop, 
            rate_limit=rate_limit
    )
# Execute
trading_commands.execute_order(master_valuemap)
# Lock the GIL until trade is executed.
response_listener.wait_events()
```

Check out the `/tests` directory for more examples.

Monitoring of trade execution is carried out using the `OrderMoitor` class, which is updated by the `TableListener`.

```python
order_monitor = session_handler.get_order_monitor()

orders = order_monitor.get_monitors()
```

Each `trade_id` has its own monitoring class, with each subsequent order appended to the initial trade conveniently wrapped in a dictionary.

```python
monitors = order_monitor.get_monitors()

{'91133665': <fxcpy.listeners.order.Order at 0x7fa038068630>,
 '91133774': <fxcpy.listeners.order.Order at 0x7fa038068668>,
 '91145522': <fxcpy.listeners.order.Order at 0x7fa038068cf8>,
 '91145541': <fxcpy.listeners.order.Order at 0x7fa038068cc0>,
 ...
 ...}

# Access using trade_id
order = monitors['91133665']

order.get_result()

"Executed"

order.get_state()

"OrderExecuted"
```

To close all positions at the current market price, extract trade attributes from the `TradesTable` class.

```python
master_valuemap = trading_commands.create_valuemap()
for trade_id, offer_id in trades_table.get_trade_ids().items():
    direction = trades_table.get_buysell(trade_id)
    if direction == 'B':
        buysell = 'S'
    else: # direction == 'S'
        buysell = 'B'
    amount = trades_table.get_amount(trade_id)
    child_valuemap = trading_commands.create_close_market_order(
        offer_id,
        buysell,
        trade_id=trade_id,
        amount=amount,
        net_quantity='N'
    )
    master_valuemap.appendChild(child_valuemap)
trading_commands.execute_order(master_valuemap)
response_listener.wait_events()
```

### Price History

FXCM has tons of free data, and the `MarketData` class will provide access to these data.

Note:

* FXCM servers will never return more than 300 bars of data in one API call.  
* All datetime is stored in UTC and of type OLE automation, for instance `float(0.0) = datetime(1899,12,30)`, take a look in the utils directory.  

```python
from datetime import datetime
from fxcpy.utils.date_utils import to_ole

market_data = session_handler.get_market_data()

data_gen = market_data.get_price_data("GBP/USD", "D1", 0.0, to_ole(datetime.utcnow()))

data = next(data_gen)
print(data)
```

Generator returns a structured numpy array.

```python
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
```

### Development

There is a lot of testing to be completed, and I am slowly working on it in my spare time.

Feel free to offer advice on any improvements.

# License Terms  

## Copyright (c) 2018 James K Bowler  

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.  

# Forex Trading Disclaimer  
Trading foreign exchange on margin carries a high level of risk, and may not be suitable for all investors. Past performance is not indicative of future results. The high degree of leverage can work against you as well as for you. Before deciding to invest in foreign exchange you should carefully consider your investment objectives, level of experience, and risk appetite. The possibility exists that you could sustain a loss of some or all of your initial investment and therefore you should not invest money that you cannot afford to lose. You should be aware of all the risks associated with foreign exchange trading, and seek advice from an independent financial advisor if you have any doubts.
