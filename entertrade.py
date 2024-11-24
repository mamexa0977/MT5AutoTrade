import MetaTrader5 as mt5
import time
import os

# File path for sharing data
DATA_FILE = 'trade_data.txt'
def get_current_price(symbol):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Symbol {symbol} information not available.")
        return None
    return symbol_info.bid, symbol_info.ask
def enter_trade(order_type, entry, sl, tp):
    # Initialize and login to MetaTrader5
    mt5.initialize()

    # login = 5024907906
    # password = ''
    login = 81478736
    password = ''
    server = 'MetaQuotes-Demo'

    authorized = mt5.login(login, password, server)

    if not authorized:
        print("Failed to connect to account, error:", mt5.last_error())
        quit()
    else:
        print("Connected to MetaTrader5")

    # Get symbol information directly for XAUUSD (skip symbol list retrieval)
    symbol = 'XAUUSD'
    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        print(f"Symbol {symbol} information not available.")
        quit()  # Exit if symbol information isn't available

    # Define market order parameters
    
    current_bid, current_ask = get_current_price('XAUUSD')
    if current_bid is None or current_ask is None:
        print("Failed to get current price of XAUUSD.")
        mt5.shutdown()
        return

    # Define market order parameters
    volume = 0.1
    action = mt5.TRADE_ACTION_DEAL
    entry = current_bid if order_type == 'SELL' else current_ask   # Entry price provided by the user

    stop_loss = sl  # Stop loss provided by the user
    # take_profit = tp  # Take profit provided by the user

    # Determine order type
    if order_type == 'BUY':
        order_type_mt5 = mt5.ORDER_TYPE_BUY
        tp_price = current_bid + 3 
    elif order_type == 'SELL':
        order_type_mt5 = mt5.ORDER_TYPE_SELL
        tp_price = current_ask - 3
    else:
        print("Invalid order type.")
        return
    tp_price = max(tp_price, 0)
    take_profit = tp_price
    # Create market order request
    request = {
        "action": action,
        "symbol": symbol,
        "volume": volume,
        "type": order_type_mt5,
        "price": entry,
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

