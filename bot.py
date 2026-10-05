import os
import random
import asyncio
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands


TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_NAME = "general"


POLLS = [
    ("What's your favorite Minecraft mode?", ["Survival", "Creative", "Hardcore", "PvP"]),
    ("Which game do you play the most?", ["Minecraft", "Roblox", "Fortnite", "Other"]),
    ("What's better?", ["Pizza", "Burger", "Both", "Neither"]),
    ("What time do you usually play games?", ["Morning", "Afternoon", "Evening", "Night"]),
    ("Which Minecraft dimension is best?", ["Overworld", "Nether", "End", "All of them"]),
    ("What's your favorite PvP weapon?", ["Sword", "Axe", "Bow", "Other"]),
    ("How active are you on Discord?", ["Very active", "Pretty active", "Sometimes", "Rarely"]),
    ("What's your favorite type of music?", ["Funk", "Rap", "EDM", "Other"]),
    ("Would you rather?", ["Better PC", "Better phone", "Better internet", "More storage"]),
    ("What's your favorite school subject?", ["Maths", "Science", "English", "Other"]),
    ("Which is better?", ["Summer", "Winter", "Rainy season", "Depends"]),
    ("How long do you usually game?", ["<1 hour", "1–2 hours", "2–4 hours", "4+ hours"]),
    ("What's your favorite Minecraft activity?", ["Building", "PvP", "Mining", "Exploring"]),
    ("Which is more important in a PC?", ["CPU", "GPU", "RAM", "Storage"]),
    ("What's your favorite snack?", ["Chips", "Chocolate", "Biscuits", "Other"]),
    ("Would you rather have?", ["Infinite FPS", "Infinite storage", "Infinite internet", "Infinite battery"]),
    ("Which game should we play together?", ["Minecraft", "L4D", "Roblox", "Other"]),
    ("What's your favorite time of day?", ["Morning", "Afternoon", "Evening", "Night"]),
    ("How good is your aim?", ["Insane", "Good", "Average", "Terrible 💀"]),
    ("What's more annoying?", ["Lag", "High ping", "Crashes", "Updates"]),
    ("Which Minecraft update do you prefer?", ["Older versions", "Modern versions", "Both", "Don't care"]),
    ("What's your favorite server activity?", ["PvP", "Survival", "Minigames", "Chatting"]),
    ("Would you rather?", ["1000 FPS", "0 ping", "Infinite RAM", "Infinite storage"]),
    ("What's your favorite drink?", ["Water", "Juice", "Soda", "Other"]),
    ("Which do you use more?", ["PC", "Phone", "Console", "Tablet"]),
    ("How often do you check Discord?", ["Constantly", "Every few hours", "Once a day", "Rarely"]),
    ("What's better for gaming?", ["Keyboard + mouse", "Controller", "Both", "Depends"]),
    ("What's your favorite Minecraft mob?", ["Creeper", "Zombie", "Skeleton", "Other"]),
    ("What's your biggest gaming problem?", ["Lag", "Low FPS", "Storage", "Skill issue 💀"]),
    ("Rate this server!", ["10/10", "8/10", "6/10", "Needs improvement"]),
]


last_poll = None

intents = discord.Intents.default()


class PollBot(commands.Bot):
    async def setup_hook(self):
        asyncio.create_task(send_daily_poll())


bot = PollBot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Daily poll system is running.")


async def send_daily_poll():
    global last_poll

    await bot.wait_until_ready()

    while not bot.is_closed():
        now = datetime.now(timezone.utc)

        # 8:05 PM IST = 14:35 UTC
        target = now.replace(
            hour=14,
            minute=35,
            second=0,
            microsecond=0
        )

        if now >= target:
            target += timedelta(days=1)

        wait_seconds = (target - now).total_seconds()

        print(f"Next poll in {wait_seconds / 3600:.2f} hours.")

        await asyncio.sleep(wait_seconds)

        for guild in bot.guilds:
            channel = discord.utils.get(
                guild.text_channels,
                name=CHANNEL_NAME
            )

            if channel is None:
                print(f"Could not find #{CHANNEL_NAME} in {guild.name}")
                continue

            available = [
                poll for poll in POLLS
                if poll != last_poll
            ]

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

                print(
                    f"Poll posted in {guild.name}: {question}"
                )

            except Exception as e:
                print(
                    f"Could not create poll in {guild.name}: {e}"
                )


async def main():
    async with bot:
        await bot.start(TOKEN)


asyncio.run(main())
