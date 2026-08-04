import os
import random
import string
import threading

from flask import Flask
import discord
from discord.ext import commands, tasks

TOKEN = os.getenv("TOKEN")

CHANNEL_ID = 1534197038391230626  # Replace with your Discord channel ID

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.all()
)

current_key = ""

def create_key():
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(50))

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

    if not key_refresh.is_running():
        key_refresh.start()

@tasks.loop(minutes=15)
async def key_refresh():
    global current_key

    current_key = create_key()

    channel = bot.get_channel(CHANNEL_ID)

    if channel:
        await channel.send(
            f"🔑 **New Key Generated**\n\n"
            f"`{current_key}`\n\n"
            f"⏰ **This key will expire in 15 minutes.**"
        )

threading.Thread(target=run_web, daemon=True).start()

bot.run(TOKEN)
