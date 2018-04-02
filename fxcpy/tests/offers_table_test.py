from fxcpy.utils.date_utils import fm_ole
from fxcpy.session_handler import SessionHandler

from fxcpy.trading_tables.offers_table import OffersTable

from fxcpy.settings import USER, PASS, URL, ENV

import pandas as pd 

session_handler = SessionHandler(USER, PASS, URL, ENV, True)
table_manager = session_handler.table_manager
ot = OffersTable(table_manager)

df_list = []
# Test all functions
for symbol, offer_id in ot.get_offer_ids().items():
    d = {}
    d[ot.get_instrument(offer_id)] = {
        "offer_id" : offer_id,
        "ask" : ot.get_ask(offer_id),
        "bid" : ot.get_bid(offer_id),
        "ask_t" : ot.get_ask_tradable(offer_id),
        "bid_t" : ot.get_bid_tradable(offer_id),
        "buy_int" : ot.get_buy_interest(offer_id),
        "contract" : ot.get_contract_currency(offer_id),
        "con_multi" : ot.get_contract_multiplier(offer_id),
        "digits" : ot.get_digits(offer_id),
        "high" : ot.get_high(offer_id),
        "type" : ot.get_instrument_type(offer_id),
        "low" : ot.get_low(offer_id),
        "point_size" : ot.get_point_size(offer_id),
        "quote_id" : ot.get_quote_id(offer_id),
        "sell_int" : ot.get_sell_interest(offer_id),
        "sub_status" : ot.get_subscription_status(offer_id),
        "time" : fm_ole(ot.get_time(offer_id)),
        "tra_status" : ot.get_trading_status(offer_id),
        "value_date" : fm_ole(ot.get_value_date(offer_id)),
        "volume" : ot.get_volume(offer_id),
        "offer_id_valid" : ot.is_offer_id_valid(offer_id),
        "instrument_valid" : ot.is_instrument_valid(offer_id),
        "quote_id_valid" : ot.is_quote_id_valid(offer_id),
        "bid_valid" : ot.is_bid_valid(offer_id),
        "ask_valid" : ot.is_ask_valid(offer_id),
        "low_valid" : ot.is_low_valid(offer_id),
        "high_valid" : ot.is_high_valid(offer_id),
        "volume_valid" : ot.is_volume_valid(offer_id),
        "time_valid" : ot.is_time_valid(offer_id),
        "bid_tradable_valid" : ot.is_bid_tradable_valid(offer_id),
        "ask_tradable_valid" : ot.is_ask_tradable_valid(offer_id),
        "sell_interest_valid" : ot.is_sell_interest_valid(offer_id),
        "buy_interest_valid" : ot.is_buy_interest_valid(offer_id),
        "contract_currency_valid" : ot.is_contract_currency_valid(offer_id),
        "digits_valid" : ot.is_digits_valid(offer_id),
        "point_size_valid" : ot.is_point_size_valid(offer_id),
        "subscription_status_valid" : ot.is_subscription_status_valid(offer_id),
        "instrument_type_valid" : ot.is_instrument_type_valid(offer_id),
        "contract_multiplier_valid" : ot.is_contract_multiplier_valid(offer_id),
        "trading_status_valid" : ot.is_trading_status_valid(offer_id),
        "value_date_valid" : ot.is_value_date_valid(offer_id)
    }
    df = pd.DataFrame(
        list(d[ot.get_instrument(offer_id)].values()),
        index=d[ot.get_instrument(offer_id)],
        columns=d.keys()
    )
    df_list.append(df)

df_offers_table = pd.concat(df_list, axis=1)

print(df_offers_table['GBP/USD'])

session_handler.logout()