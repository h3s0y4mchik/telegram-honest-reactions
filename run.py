import asyncio
import customtkinter as ctk
from pyrogram import Client, filters
from pyrogram.types import Message
from random import choice
import json
import os
import threading
import sys

# Global variables
TARGET_USERS = []
EMOJI_LIST = []
api_id = ""
api_hash = ""
bot_running = False
bot_app = None

# Path to settings file
SETTINGS_FILE = "settings.json"

# Load settings
def load_settings():
    global TARGET_USERS, EMOJI_LIST, api_id, api_hash
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
                TARGET_USERS = settings.get("users", [])
                EMOJI_LIST = settings.get("emojis", [])
                api_id = settings.get("api_id", "")
                api_hash = settings.get("api_hash", "")
            log_message("Settings loaded successfully.")
        except Exception as e:
            log_message(f"Error loading settings: {str(e)}", "error")

# Save settings
def save_settings():
    settings = {
        "users": TARGET_USERS,
        "emojis": EMOJI_LIST,
        "api_id": api_id,
        "api_hash": api_hash
    }
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        log_message("Settings saved successfully.")
    except Exception as e:
        log_message(f"Error saving settings: {str(e)}", "error")

# Log messages
def log_message(message, level="info"):
    if not gui_mode:  # If not in GUI mode, print directly to the console
        print(f"[{level.upper()}] {message}")
    else:
        log_box.insert("end", f"[{level.upper()}] {message}\n")
        log_box.yview("end")  # Scroll to the end

# Asynchronous bot start
async def start_bot(api_id, api_hash):
    await process_input()
    global bot_running, bot_app
    bot_running = True
    bot_app = Client("my_account", api_id=api_id, api_hash=api_hash)

    @bot_app.on_message(filters.private & filters.incoming)
    async def react_to_message(client: Client, message: Message):
        username = message.from_user.username
        if message.from_user.id in TARGET_USERS or username in TARGET_USERS or f'@{username}' in TARGET_USERS:
            emoji = choice(EMOJI_LIST)
            try:
                await bot_app.send_reaction(chat_id=message.chat.id, message_id=message.id, emoji=emoji)
                log_message(f"Added reaction {emoji} to message from {message.from_user.username or message.from_user.id}")
            except Exception as e:
                log_message(f"Error while adding reaction: {str(e)}", "error")

    await bot_app.start()
    log_message(f"Bot started.")

# Asynchronous bot stop
async def stop_bot():
    global bot_running, bot_app
    if bot_running:
        await bot_app.stop()
        bot_running = False
        log_message("Bot stopped.")

# Toggle bot start/stop
def toggle_bot():
    global bot_running
    if bot_running:
        log_message("Stopping bot...")
        loop.call_soon_threadsafe(lambda: asyncio.create_task(stop_bot()))  # Stop bot
        start_button.configure(text="Start Bot")
    else:
        log_message("Starting bot...")
        start_button.configure(text="Stop Bot")
        loop.call_soon_threadsafe(lambda: asyncio.create_task(start_bot(api_id, api_hash)))  # Start bot

# Handle input and start the bot
async def process_input():
    global TARGET_USERS, EMOJI_LIST, api_id, api_hash
    
    user_input = []
    emoji_input = []
    api_id_input = ""
    api_hash_input = ""
    
    if not TARGET_USERS or not EMOJI_LIST or not api_id or not api_hash:

        # Get values from the input fields or console
        user_input = user_ids_input.get().strip().split() if gui_mode else input("Enter user IDs or usernames (separate by space): ").strip().split()
        emoji_input = emoji_list_input.get().strip().split() if gui_mode else input("Enter emojis (separate by space): ").strip().split()

        # Check for API keys
        api_id_input = api_id_input.get().strip() if gui_mode else input("Enter API ID: ").strip()
        api_hash_input = api_hash_input.get().strip() if gui_mode else input("Enter API Hash: ").strip()

        if not api_id_input or not api_hash_input:
            log_message("API ID and API Hash are required!", "error")
            return
    else:
        user_input = TARGET_USERS
        emoji_input = EMOJI_LIST
        api_id_input = api_id
        api_hash_input = api_hash

    # Split `user_id` and `username`
    TARGET_USERS = []
    for item in user_input:
        if item.isdigit():  # If it's an ID
            TARGET_USERS.append(int(item))
        else:  # If it's a username
            TARGET_USERS.append(item)

    # Save emoji list
    EMOJI_LIST = emoji_input

    log_message(f"Users: {TARGET_USERS}")
    log_message(f"Emojis: {EMOJI_LIST}")

    # Save settings
    save_settings()

# Start asyncio loop in a separate thread
def start_async_loop():
    global loop
    loop = asyncio.new_event_loop()  # New event loop for this thread
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Exit the application
def exit_application():
    root.quit()  # Stop the Tkinter main loop
    loop.stop()  # Stop the asyncio event loop

# Set up customtkinter (only in GUI mode)
def setup_gui():
    global gui_mode
    gui_mode = True  # Mark that we are in GUI mode
    ctk.set_appearance_mode("System")  # Can choose "Light", "Dark", "System"
    ctk.set_default_color_theme("blue")  # Can choose themes: "blue", "green", "dark-blue"

    # Create the main window and controls
    global root, api_id_input, api_hash_input, user_ids_input, emoji_list_input, start_button, exit_button, log_box
    root = ctk.CTk()

    root.title("Bot Setup")

    # API ID input
    api_id_label = ctk.CTkLabel(root, text="Enter API ID:")
    api_id_label.pack(pady=10)
    api_id_input = ctk.CTkEntry(root, width=300)
    api_id_input.pack(pady=10)

    # API Hash input
    api_hash_label = ctk.CTkLabel(root, text="Enter API Hash:")
    api_hash_label.pack(pady=10)
    api_hash_input = ctk.CTkEntry(root, width=300)
    api_hash_input.pack(pady=10)

    # User input
    user_label = ctk.CTkLabel(root, text="Enter usernames or user_ids (separate by space):")
    user_label.pack(pady=10)
    user_ids_input = ctk.CTkEntry(root, width=300)
    user_ids_input.pack(pady=10)

    # Emoji input
    emoji_label = ctk.CTkLabel(root, text="Enter emojis (separate by space):")
    emoji_label.pack(pady=10)
    emoji_list_input = ctk.CTkEntry(root, width=300)
    emoji_list_input.pack(pady=10)

    # Start/Stop button for the bot
    start_button = ctk.CTkButton(root, text="Start Bot", command=toggle_bot)
    start_button.pack(pady=20)

    # Exit button to close the app
    exit_button = ctk.CTkButton(root, text="Exit", command=exit_application)
    exit_button.pack(pady=10)

    # Log box for debug messages
    log_label = ctk.CTkLabel(root, text="Log:")
    log_label.pack(pady=10)

    log_box = ctk.CTkTextbox(root, width=300, height=150)
    log_box.pack(pady=10)

    # Load settings at startup
    load_settings()

    # Pre-fill the input fields if settings are available
    if api_id:
        api_id_input.insert(0, api_id)
    if api_hash:
        api_hash_input.insert(0, api_hash)
    if TARGET_USERS:
        user_ids_input.insert(0, " ".join(map(str, TARGET_USERS)))
    if EMOJI_LIST:
        emoji_list_input.insert(0, " ".join(EMOJI_LIST))

    # Start the asyncio event loop in a separate thread
    threading.Thread(target=start_async_loop, daemon=True).start()

    # Start the Tkinter main loop
    root.mainloop()

# Command-line mode setup
def setup_cli():
    global gui_mode
    gui_mode = False  # Mark that we are in CLI mode
    load_settings()  # Try loading settings
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    if not TARGET_USERS or not EMOJI_LIST or not api_id or not api_hash:
        log_message("Starting without GUI. You must input necessary details.")
        loop.run_until_complete(process_input())  # Process input via console
    
    try:
        loop.run_until_complete(start_bot(api_id, api_hash))
        # Start the asyncio event loop
        loop.run_forever()
    except KeyboardInterrupt:
        # Stop the asyncio event loop on keyboard interrupt
        log_message("Stopping bot...", "info")
        loop.run_until_complete(stop_bot())
        loop.close()

# Entry point of the program
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--no-gui":
        setup_cli()  # Start without GUI if the argument is provided
    else:
        setup_gui()  # Default to GUI mode
