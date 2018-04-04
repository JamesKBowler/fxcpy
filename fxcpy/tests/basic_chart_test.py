from fxcpy.session_handler import SessionHandler
from fxcpy.chart.basic_chart import BasicChart
from fxcpy.settings import USER, PASS, URL, ENV
from datetime import datetime, timedelta

session_handler = SessionHandler(USER, PASS, URL, ENV, True)
market_data = session_handler.get_market_data()

# Collection attribs
dtto = datetime.utcnow()
dtfm = dtto - timedelta(days=200)
instrument = "GBP/USD"
time_frame = "D1"

# Plot chart
BasicChart(market_data).graph(instrument, time_frame, dtfm, dtto)