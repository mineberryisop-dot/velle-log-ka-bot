import os
import random
import asyncio
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands

TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_NAME = "general"

POLLS = [
    ("What's your favorite game?", ["Minecraft", "Roblox", "Valorant", "Other"]),
    ("How cooked are you for your next exam?", ["Fine", "A little cooked", "Deep fried", "Absolutely finished 💀"]),
    ("What do you usually do after school?", ["Game", "Study", "Sleep", "Scroll"]),
    ("Which is more annoying?", ["Lag", "Bad teammates", "Sweats", "Bugs"]),
    ("Would you rather have:", ["0 ping forever", "Unlimited FPS forever"]),
    ("What's your usual sleep time?", ["Before 10 PM", "10–12", "12–2", "2+ 💀"]),
    ("Which one would you choose?", ["₹10 lakh now", "₹1 crore in 10 years"]),
    ("What should the server do more often?", ["Polls", "Events", "Gaming", "Memes"]),
    ("How active are you on Discord?", ["Very active", "Sometimes", "Rarely", "I forgot this server existed 💀"]),
    ("What's your favorite Minecraft mode?", ["Survival", "PvP", "Skyblock", "Creative"]),
]

last_poll = None


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


async def send_daily_poll():
    global last_poll

    await bot.wait_until_ready()

    while not bot.is_closed():
        now = datetime.now(timezone.utc)

        # 7:00 PM IST = 13:30 UTC
        target = now.replace(hour=13, minute=30, second=0, microsecond=0)

        if now >= target:
            target += timedelta(days=1)

        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        for guild in bot.guilds:
            channel = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)

            if channel is None:
                continue

            available = [p for p in POLLS if p != last_poll]

            if not available:
                available = POLLS

            poll = random.choice(available)
            last_poll = poll

            question, answers = poll

            try:
                await channel.create_poll(
                    question=question,
                    answers=[
                        discord.PollAnswer(text=answer)
                        for answer in answers
                    ],
                    duration=24,
                    multiple=False
                )
            except Exception as e:
                print(f"Could not create poll: {e}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Daily poll system is running.")


async def main():
    async with bot:
        bot.loop.create_task(send_daily_poll())
        await bot.start(TOKEN)


asyncio.run(main())
