# Telegram Trading Bot

This project automates the process of fetching trading signals from a Telegram channel, sending them to an AI bot for further analysis, and executing the trade on MetaTrader5 based on the AI's response.

## Features
- Fetches trading signals from specified Telegram channels.
- Sends signals to an AI chatbot to analyze the entry, stop loss (SL), and take profit (TP) values.
- Extracts the response from the AI bot and writes the trade data to a file.
- Monitors the trade data file and places market orders on MetaTrader5.

## Requirements
Before running the bot, ensure that you have the following:
- Python 3.x installed
- MetaTrader5 installed and set up with a valid account
- Telegram API credentials (API ID and API hash)
- MetaTrader5 Python package (`MetaTrader5`)

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/mamexa0977/MT5AutoTrade.git
   cd MT5AutoTrade

## Install the required dependencies:
         ```bash
         pip install telethon MetaTrader5

## Replace the following placeholders in the script:

- `api_id`: Your Telegram API ID
- `api_hash`: Your Telegram API hash
- `TARGET_CHANNEL_USERNAME_1`, `TARGET_CHANNEL_USERNAME_2`: The Telegram channel usernames to fetch signals from
- `AI_BOT_USERNAME`: The username of the AI bot used for signal analysis
- `DATA_FILE`: The file path for storing trade data


Ensure you have access to a MetaTrader5 account and replace the login, password, and server in the enter_trade function with your actual login details.

## Usage

The bot will start listening for new messages in the specified Telegram channels. When a valid signal is found, it will be sent to the AI bot for analysis. Once the AI bot responds, the bot will place a market order on MetaTrader5.

The bot continues running and processes trade signals as long as the script is active.

## How It Works
Telegram Signal Fetching: The bot listens for new messages in the specified channels. If the message contains the keywords "BUY", "SELL", "GOLD", or "XAUUSD" with a stop loss (SL), the bot sends the signal to an AI bot for analysis.

AI Bot Response Parsing: The bot extracts the Entry, SL, and TP1 values from the AI bot's response and writes them to a file.

Trade Execution: The bot reads the trade data from the file, connects to MetaTrader5, and places a market order based on the extracted values.

## MetaTrader5 Integration
The bot uses the MetaTrader5 package to interact with the MetaTrader5 terminal and execute market orders based on the signal data.
Ensure that the MetaTrader5 terminal is running and connected to the correct server before executing the bot.
## Notes
Ensure the AI bot you are using can parse and respond to the signal format specified in the script.
The script is currently designed to work with the XAUUSD symbol on MetaTrader5. Adjust the symbol if you wish to trade other instruments.
Error handling and retries are in place to ensure the bot operates smoothly.
