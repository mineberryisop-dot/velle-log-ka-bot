import os
import random
import asyncio
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands

TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_NAME = "general"

POLLS = [
    ("What's your favorite type of weather?", ["Rainy", "Sunny", "Cloudy", "Cold"]),
    ("What's better?", ["Tea", "Coffee", "Neither", "Both"]),
    ("What's your favorite time of day?", ["Morning", "Afternoon", "Evening", "Night"]),
    ("Could you survive a week without your phone?", ["Easily", "Probably", "Maybe", "Absolutely not 💀"]),
    ("What's the best way to spend a free day?", ["Go outside", "Stay home", "Meet friends", "Sleep"]),
    ("Which do you prefer?", ["Movies", "TV shows", "YouTube", "Short videos"]),
    ("What's your favorite season?", ["Summer", "Winter", "Spring", "Autumn"]),
    ("What's better?", ["Beach", "Mountains", "City", "Countryside"]),
    ("How often do you listen to music?", ["All day", "Often", "Sometimes", "Rarely"]),
    ("What's your favorite type of food?", ["Fast food", "Homemade", "Street food", "Anything 😭"]),
    ("What's the best snack?", ["Chips", "Chocolate", "Biscuits", "Popcorn"]),
    ("What's your favorite drink?", ["Water", "Juice", "Soda", "Tea/Coffee"]),
    ("Would you rather have:", ["Free food forever", "Free travel forever"]),
    ("Would you rather:", ["Always be 10 minutes early", "Always be 10 minutes late"]),
    ("What's more important?", ["Money", "Free time", "Friends", "Happiness"]),
    ("Which sounds better?", ["Big party", "Small hangout", "Going somewhere", "Staying home"]),
    ("Do you prefer working alone or with others?", ["Alone", "With others", "Depends", "Neither 💀"]),
    ("What's your ideal weekend?", ["Going out", "Staying home", "Seeing friends", "Doing absolutely nothing"]),
    ("How often do you take photos?", ["All the time", "Sometimes", "Rarely", "Never"]),
    ("What's your favorite kind of video?", ["Funny", "Informative", "Interesting", "Random"]),
    ("Which would you choose?", ["Teleportation", "Time travel", "Invisibility", "Mind reading"]),
    ("Would you rather have:", ["Unlimited money", "Unlimited free time"]),
    ("What's more annoying?", ["Waiting", "Noise", "Slow internet", "Being interrupted"]),
    ("What's your usual mood when you wake up?", ["Happy", "Tired", "Confused", "Don't talk to me 💀"]),
    ("How long could you go without social media?", ["A day", "A week", "A month", "Forever"]),
    ("What's better?", ["Sweet food", "Spicy food", "Salty food", "Sour food"]),
    ("What's your favorite type of movie?", ["Comedy", "Action", "Horror", "Drama"]),
    ("Would you rather live in:", ["A huge city", "A small town", "The countryside", "Somewhere random"]),
    ("What's your biggest enemy?", ["Alarm clocks", "Homework/work", "Traffic", "Monday"]),
    ("What's more satisfying?", ["Finishing a task", "Getting something new", "Eating good food", "Sleeping"]),
]

last_poll = None

intents = discord.Intents.default()


class PollBot(commands.Bot):
    async def setup_hook(self):
        asyncio.create_task(send_daily_poll())


bot = PollBot(command_prefix="!", intents=intents)


async def send_daily_poll():
    global last_poll

    await bot.wait_until_ready()

    while not bot.is_closed():
        now = datetime.now(timezone.utc)

        # 7:00 PM IST = 13:30 UTC
        target = now.replace(
            hour=13,
            minute=30,
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

            available = [poll for poll in POLLS if poll != last_poll]

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

                print(f"Poll posted in {guild.name}: {question}")

            except Exception as e:
                print(f"Could not create poll: {e}")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Daily poll system is running.")


async def main():
    async with bot:
        await bot.start(TOKEN)


asyncio.run(main())
