# Telegram Honest Reactions Bot

A simple Telegram bot that adds random emoji reactions to messages from specific users based on their username or user ID. The bot allows you to configure the list of target users and emojis and provides a graphical interface for easy setup.

## Features

- Add emoji reactions to messages from selected users.
- Configure target users and emojis through a simple graphical interface.
- Save and load configuration settings for future use.
- Start and stop the bot via the interface.
- Log all events and actions in real time.

## Requirements

Before running the bot, you need to install the following dependencies:

- Python 3.7 or higher
- [Pyrogram](https://docs.pyrogram.org/) for interacting with the Telegram API
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) for the graphical user interface
- [asyncio](https://docs.python.org/3/library/asyncio.html) (usually pre-installed with Python)

To install the necessary Python packages, run:

```bash
pip install pyrogram customtkinter
```

## Setup

1. Obtain your **API ID** and **API Hash** from [Telegram's API development tools](https://my.telegram.org/apps).
2. Clone this repository:
```bash
git clone https://github.com/yourusername/telegram-honest-reactions.git
cd telegram-honest-reactions
```
3. Run the script to start the graphical interface:
```bash
python run.py
```
4. Enter your **API ID** and **API Hash**, as well as the list of target users (usernames or user IDs) and emojis (separate by spaces).
5. Click the "Start Bot" button to begin using the bot.

## Usage
- After starting the bot, it will react to messages from the specified users with random emojis.
- You can stop the bot by clicking the "Stop Bot" button in the interface.
- The bot will save your settings (API ID, API Hash, users, and emojis) for future use, so you don't have to re-enter them each time.

## License
This project is licensed under the MIT License - see the LICENSE file for details.