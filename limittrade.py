import MetaTrader5 as mt5
import time
import os

# File path for sharing data
DATA_FILE = 'trade_data.txt'

def initialize_and_login(login, password, server):
    # Initialize and login to MetaTrader5
    mt5.initialize()
    authorized = mt5.login(login, password, server)
    if not authorized:
        print("Failed to connect to account, error:", mt5.last_error())
        return False
    print("Connected to MetaTrader5")
    return True

def enter_trade(order_type, entry, sl, tp):
    login = 1503672
    password = ''
    server = 'ACGMarkets-Live'

    if not initialize_and_login(login, password, server):
        quit()  # Exit if login fails

    # Get symbol information for XAUUSD.pro
    symbol = 'XAUUSD.pro'
    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        print(f"Symbol {symbol} information not available.")
        quit()  # Exit if symbol information isn't available

    # Define market order parameters
    volume = 0.1
    action = mt5.TRADE_ACTION_DEAL
    stop_loss = sl
    take_profit = tp

    # Determine order type and price
    if order_type == 'BUY':
        price = symbol_info.ask
        order_type_mt5 = mt5.ORDER_TYPE_BUY
    elif order_type == 'SELL':
        price = symbol_info.bid
        order_type_mt5 = mt5.ORDER_TYPE_SELL
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
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Send market order request
    res = mt5.order_send(request)

    if res is None:
        print("Failed to place market order:", mt5.last_error())
    else:
        print("Market Order Result:", res)

    # Disconnect from MetaTrader5
    mt5.shutdown()

def monitor_data_file():
    while True:
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

if __name__ == "__main__":
    monitor_data_file()
