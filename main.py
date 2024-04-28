from telethon import TelegramClient, events
import re
import time
import asyncio
import os

# Replace with your Telegram API credentials
api_id = 26893943
api_hash = '2ca18ff57d54538125b02144f66738ba'

# Target channel username (replace with the actual channel username)
TARGET_CHANNEL_USERNAME = 'https://t.me/mamexfxsignal'

# AI chat bot username (replace with the actual bot username)
AI_BOT_USERNAME = '@Free_of_ChatGPT_bot'

# File path for sharing data
DATA_FILE = 'trade_data.txt'

async def main():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        print("Bot started.")

        @client.on(events.NewMessage(chats=TARGET_CHANNEL_USERNAME))
        async def handler(event):
            message = event.message
            # Check if message contains signal keywords
            if any(word in message.message.upper() for word in ['BUY', 'SELL']):
                signal_message = f"""give me the entry closest to sl, sl, tp2, and order type,
                 {message.message}
                 the structure of your answer is like this .
                 "order buyorsell
                 Entry thenumber
                 Sl thenumber
                 tp2 thenumber " 
                 not another explanation is needed"""
                # Send the signal message to the AI bot
                try:
                    await client.send_message(AI_BOT_USERNAME, signal_message)
                    print("Signal message sent to the AI bot.")
                except Exception as e:
                    print(f"Failed to send signal message to the AI bot: {e}")

        @client.on(events.NewMessage(chats=AI_BOT_USERNAME))
        async def bot_response_handler(event):
            message = event.message
            # Extract entry, sl, tp2, and order type from the bot's response
            entry_match = re.search(r'Entry\s+(\d+(?:\.\d+)?)', message.message, re.IGNORECASE)
            sl_match = re.search(r'SL\s+(\d+(?:\.\d+)?)', message.message, re.IGNORECASE)
            tp2_match = re.search(r'TP2\s+(\d+(?:\.\d+)?)', message.message, re.IGNORECASE)
            order_type_match = re.search(r'order\s+(BUY|SELL)', message.message, re.IGNORECASE)
            time.sleep(3)
            if entry_match and sl_match and tp2_match and order_type_match:
                entry = float(entry_match.group(1))
                sl = float(sl_match.group(1))
                tp2 = float(tp2_match.group(1))
                order_type = order_type_match.group(1).upper()
                print(f"Order Type: {order_type}, Entry: {entry}, SL: {sl}, TP2: {tp2}")

                # Write the received values to the data file
                with open(DATA_FILE, 'w') as f:
                    f.write(f"{order_type},{entry},{sl},{tp2}")

            else:
                print("Failed to extract entry, SL, TP2, or order type from the bot's response.")

        # Keep the script running until disconnected
        print("Bot is running. Press Ctrl+C to stop.")
        await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
