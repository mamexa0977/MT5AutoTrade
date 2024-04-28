
# import MetaTrader5 as mt5

# # initialize and login to MetaTrader5
# mt5.initialize()

# login = 5024907906
# password = 'NiY!Bv4f'
# server = 'MetaQuotes-Demo'

# authorized = mt5.login(login, password, server)

# if not authorized:
#     print("Failed to connect to account, error:", mt5.last_error())
#     quit()
# else:
#     print("Connected to MetaTrader5")

# # Get symbol information directly for EURUSD (skip symbol list retrieval)
# symbol = 'XAUUSD'
# symbol_info = mt5.symbol_info(symbol)

# if symbol_info is None:
#     print(f"Symbol {symbol} information not available.")
#     quit()  # Exit if symbol information isn't available

# # Define market order parameters
# volume = 0.1
# action = mt5.TRADE_ACTION_DEAL
# order_type = None  # Initialize order type variable

# # Entry price provided by the user (replace this with the actual value)
# entry_price = 1.1000

# # Determine whether the order is a buy or sell order (replace this with your logic)
# is_buy_order = False  # Change to False if it's a sell order

# # Determine whether to place a buy limit/buy stop or sell limit/sell stop order based on the current price
# current_price = symbol_info.bid
# if is_buy_order:
#     if entry_price < current_price:
#         order_type = mt5.ORDER_TYPE_BUY_LIMIT
#         price = entry_price
#     else:
#         order_type = mt5.ORDER_TYPE_BUY_STOP
#         price = entry_price
# else:
#     if entry_price > current_price:
#         order_type = mt5.ORDER_TYPE_SELL_LIMIT
#         price = entry_price
#     else:
#         order_type = mt5.ORDER_TYPE_SELL_STOP
#         price = entry_price

# stop_loss = 0.0  # set to 0.0 if you don't want SL
# take_profit = 0.0  # set to 0.0 if you don't want TP

# # Create market order request
# request = {
#     "action": action,
#     "symbol": symbol,
#     "volume": volume,
#     "type": order_type,
#     "price": price,
#     "sl": stop_loss,
#     "tp": take_profit,
#     "deviation": 20,
#     "magic": 0,
#     "comment": "python market order",
#     "type_time": mt5.ORDER_TIME_GTC,
#     "type_filling": mt5.ORDER_FILLING_IOC,  # Some brokers might require IOC or FOK
# }

# # Send market order request
# res = mt5.order_send(request)

# print("Market Order Result:", res)

# # Disconnect from MetaTrader5
# mt5.shutdown()

import MetaTrader5 as mt5
import time
import os

# File path for sharing data
DATA_FILE = 'trade_data.txt'

def enter_trade(order_type, entry, sl, tp):
    # Initialize and login to MetaTrader5
    mt5.initialize()

    login = 5024907906
    password = 'NiY!Bv4f'
    server = 'MetaQuotes-Demo'

    authorized = mt5.login(login, password, server)

    if not authorized:
        print("Failed to connect to account, error:", mt5.last_error())
        quit()
    else:
        print("Connected to MetaTrader5")

    # Get symbol information directly for EURUSD (skip symbol list retrieval)
    symbol = 'XAUUSD'
    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        print(f"Symbol {symbol} information not available.")
        quit()  # Exit if symbol information isn't available

    # Define market order parameters
    volume = 0.1
    action = mt5.TRADE_ACTION_DEAL
    price = entry  # Entry price provided by the user

    stop_loss = sl  # Stop loss provided by the user
    take_profit = tp  # Take profit provided by the user

    # Determine order type
    if order_type == 'BUY':
        if entry < symbol_info.bid:
            order_type_mt5 = mt5.ORDER_TYPE_BUY_LIMIT
        else:
            order_type_mt5 = mt5.ORDER_TYPE_BUY_STOP
    elif order_type == 'SELL':
        if entry > symbol_info.ask:
            order_type_mt5 = mt5.ORDER_TYPE_SELL_LIMIT
        else:
            order_type_mt5 = mt5.ORDER_TYPE_SELL_STOP
    else:
        print("Invalid order type.")
        return

    # Create market order request
    request = {
        "action": action,
        "symbol": symbol,
        "volume": volume,
        "type": order_type_mt5,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": 20,
        "magic": 0,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,  # Some brokers might require IOC or FOK
    }

    # Send market order request
    res = mt5.order_send(request)

    print("Market Order Result:", res)

    # Disconnect from MetaTrader5
    mt5.shutdown()

if __name__ == "__main__":
    while True:
        # Check if the data file exists
        if os.path.exists(DATA_FILE):
            # Read the data from the file
            with open(DATA_FILE, 'r') as f:
                data = f.readline().strip().split(',')
                order_type, entry, sl, tp = data

            # Delete the data file
            os.remove(DATA_FILE)

            # Call the enter_trade function
            enter_trade(order_type, float(entry), float(sl), float(tp))

        time.sleep(1)  # Sleep for 1 second before checking again
