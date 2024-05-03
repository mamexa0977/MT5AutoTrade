# from g4f.client import Client

# client = Client()
# response = client.chat.completions.create(
#     model="gpt-4",
#     messages=[{f"""role": "user", "content": " """}],
    
# )
# print(response.choices[0].message.content)

def standardize_signal(signal):
    signal = signal.lower()  # Convert to lowercase for case insensitivity
    parts = signal.split('\n')  # Split the signal by newlines
    order_type = ""
    entry = ""
    sl = ""
    tp = ""

    for part in parts:
        if "buy" in part:
            order_type = "Buy"
            entry = part.split("buy")[1].strip()
        elif "sell" in part:
            order_type = "Sell"
            entry = part.split("sell")[1].strip()
        elif "sl" in part:
            sl = part.split("sl")[1].strip()
        elif "tp" in part:
            tp = part.split("tp")[1].strip()
            if tp.lower() == "open":
                tp2 = "0.0"
            else:
                try:
                    tp2 = float(tp)
                except ValueError:
                    pass

    # Ensure all necessary parts are present
    if order_type and entry and sl and tp:
        standardized_signal = f"Order {order_type}\nEntry {entry}\nSl {sl}\ntp {tp}"
        return standardized_signal
    else:
        return "Signal structure is incomplete."

# Example usage
signal = """GOLD SELL NOW @2315-2319

SL 2324.00

TP 2313.09
TP 2303.90

Layering slowly use proper lot size """

standardized = standardize_signal(signal)
print(standardized)
