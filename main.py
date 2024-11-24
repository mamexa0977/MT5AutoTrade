
from telethon import TelegramClient, events
import re
import time
import asyncio
import os

# Replace with your Telegram API credentials
api_id = urid
api_hash = 'hash'

# Target channel username (replace with the actual channel username)


# TARGET_CHANNEL_USERNAME = 'https://t.me/mamexfxsignal'
TARGET_CHANNEL_USERNAME_1 = 'https://t.me/target'
TARGET_CHANNEL_USERNAME_2 = 'https://t.me/target'

# AI chat bot username (replace with the actual bot username)
AI_BOT_USERNAME = '@Free_of_ChatGPT_bot' #any ai bot 

# File path for sharing data
DATA_FILE = 'trade_data.txt'

async def main():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        print("Bot started.")

        @client.on(events.NewMessage(chats=[TARGET_CHANNEL_USERNAME_1, TARGET_CHANNEL_USERNAME_2]))
        async def handler(event):
            message = event.message
            # Check if message contains signal keywords
            if any(word in message.message.upper() for word in ['BUY', 'SELL']) and ('GOLD' in message.message.upper() or 'XAUUSD' in message.message.upper()) and 'SL' in message.message.upper():
                signal_message = f"""Give the entry closest to the stop loss (sl), stop loss (sl), take profit 1 (tp1), and order type. If tp1 is marked as 'open', then set tp1 as 0.0.
for this {message.message}
Structure your answer in the following format:
Order [Buy/Sell]
Entry [entry price]
Sl [stop loss price]
Tp1 [take profit 1 price]

No additional explanations  are needed."""
                # Send the signal message to the AI bot
                try:
                    await client.send_message(AI_BOT_USERNAME, signal_message)
                    print("Signal message sent to the AI bot.")
                except Exception as e:
                    print(f"Failed to send signal message to the AI bot: {e}")

        @client.on(events.NewMessage(chats=AI_BOT_USERNAME))
        async def bot_response_handler(event):
            message = event.message
            # # Extract entry, sl, tp1, and order type from the bot's response
            entry_match = re.search(r'Entry\s+(\d+(?:\.\d+)?)', message.message, re.IGNORECASE)
            sl_match = re.search(r'SL\s+(\d+(?:\.\d+)?)', message.message, re.IGNORECASE)
            tp1_match = re.search(r'TP1\s+(\d+(?:\.\d+)?)', message.message, re.IGNORECASE)
            order_type_match = re.search(r'order\s+(BUY|SELL)', message.message, re.IGNORECASE)
            # Extract entry, sl, tp1, and order type from the bot's response


            time.sleep(3)
            if entry_match and sl_match and tp1_match and order_type_match:
                entry = float(entry_match.group(1))
                sl = float(sl_match.group(1))
                tp1 = float(tp1_match.group(1))
                order_type = order_type_match.group(1).upper()
                print(f"Order Type: {order_type}, Entry: {entry}, SL: {sl}, TP1: {tp1}")

                # Write the received values to the data file
                with open(DATA_FILE, 'w') as f:
                    f.write(f"{order_type},{entry},{sl},{tp1}")

            else:
                print("Failed to extract entry, SL, TP1, or order type from the bot's response.")
                signal_message = f"""Give the entry closest to the stop loss (sl), stop loss (sl), take profit 1 (tp1), and order type. If tp1 is marked as 'open', then set tp1 as 0.0.
                for this {message.message}
                Structure your answer in the following format:
                Order [Buy/Sell]
            Entry [entry price]
            Sl [stop loss price]
            Tp1 [take profit 1 price]
            
            No additional explanations  are needed."""
                    
                    # Retry sending signal message to the AI bot until successful
                while True:
                        try:
                            await client.send_message(AI_BOT_USERNAME, signal_message)
                            print("Signal message sent to the AI bot.")
                            break  # Exit loop if message sent successfully
                        except Exception as e:
                            print(f"Failed to send signal message to the AI bot: {e}")
                            # Add a delay before retrying
                            await asyncio.sleep(3) 
                    # Keep the script running until disconnected
        print("Bot is running. Press Ctrl+C to stop.")
        await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())


