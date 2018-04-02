from datetime import datetime

from fxcpy.utils.date_utils import to_ole
from fxcpy.session_handler import SessionHandler
from fxcpy.factory.price_history import MarketData
from fxcpy.settings import USER, PASS, URL, ENV


session_handler = SessionHandler(USER, PASS, URL, ENV, True)

market_data = session_handler.get_market_data()

data_gen = market_data.get_price_data("GBP/USD", "H1", 0.0, to_ole(datetime.utcnow()), True)

ph = next(data_gen)
print(ph)
session_handler.logout()