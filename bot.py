```python
import os
import asyncio
import random
import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta

# ==============================
# CONFIGURATION
# ==============================

CHANNEL_NAME = "general"

# 4:30 PM IST = 11:00 AM UTC
POLL_HOUR_UTC = 11
POLL_MINUTE_UTC = 0

POLL_DURATION_HOURS = 24

# ==============================
# DAILY GENERAL POLLS
# ==============================

POLLS = [
    ("What's your favourite time of day?", ["Morning", "Afternoon", "Evening", "Night"]),
    ("Which superpower would you choose?", ["Flying", "Teleportation", "Invisibility", "Time travel"]),
    ("What's the best kind of weather?", ["Rainy", "Sunny", "Cloudy", "Cold"]),
    ("Which would you rather have?", ["Unlimited money", "Unlimited free time", "Unlimited knowledge", "Unlimited luck"]),
    ("What's your favourite type of food?", ["Pizza", "Burger", "Noodles", "Indian food"]),
    ("Which app do you use the most?", ["YouTube", "Instagram", "Discord", "WhatsApp"]),
    ("Would you rather travel to the past or future?", ["Past", "Future"]),
    ("What makes a day better?", ["Good food", "Good friends", "Good sleep", "Good news"]),
    ("Which holiday sounds best?", ["Beach trip", "Mountain trip", "City trip", "Stay at home"]),
    ("What do you prefer?", ["Texting", "Calling", "Voice chat", "Meeting in person"]),
    ("Which pet would you choose?", ["Dog", "Cat", "Bird", "Fish"]),
    ("What's the best weekend activity?", ["Gaming", "Watching movies", "Going outside", "Sleeping"]),
    ("Which drink would you pick?", ["Water", "Juice", "Cold coffee", "Tea"]),
    ("What would you do with a completely free day?", ["Sleep", "Go out", "Play games", "Watch videos"]),
    ("Which season do you prefer?", ["Summer", "Winter", "Monsoon", "Spring"]),
    ("Which matters most in a friendship?", ["Trust", "Humour", "Loyalty", "Honesty"]),
    ("Would you rather be famous or anonymous?", ["Famous", "Anonymous"]),
    ("Which sounds more fun?", ["Road trip", "Camping", "Amusement park", "Movie night"]),
    ("What is your ideal sleep schedule?", ["Early bird", "Night owl", "Somewhere in between", "No fixed schedule"]),
    ("Which would you choose?", ["Read minds", "See the future", "Stop time", "Instantly learn skills"]),
    ("What's the best kind of entertainment?", ["Movies", "Music", "Games", "Books"]),
    ("How do you usually make decisions?", ["Logic", "Feelings", "Ask someone", "Depends on the situation"]),
    ("Which would you rather explore?", ["Space", "The deep ocean", "Ancient history", "The future"]),
    ("What is your favourite kind of day?", ["Productive", "Relaxing", "Adventurous", "Unexpected"]),
    ("Which is more satisfying?", ["Finishing a task", "Learning something new", "Helping someone", "Winning a challenge"]),
    ("Would you rather live in a big city or a small town?", ["Big city", "Small town"]),
    ("Which skill would you instantly master?", ["Cooking", "Drawing", "Playing an instrument", "Speaking languages"]),
    ("What do you prefer when watching something?", ["Comedy", "Action", "Mystery", "Documentary"]),
    ("Which is more important for a great trip?", ["The destination", "The people", "The food", "The journey"]),
    ("What's your ideal way to spend an evening?", ["Listening to music", "Chatting with friends", "Watching something", "Going outside"]),
]

# ==============================
# BOT SETUP
# ==============================

intents = discord.Intents.default()

class PollBot(commands.Bot):
    async def setup_hook(self):
        asyncio.create_task(self.daily_poll_loop())

    async def daily_poll_loop(self):
        await self.wait_until_ready()

        previous_poll = None

        while not self.is_closed():
            now = datetime.now(timezone.utc)

            target = now.replace(
                hour=POLL_HOUR_UTC,
                minute=POLL_MINUTE_UTC,
                second=0,
                microsecond=0
            )

            if now >= target:
                target += timedelta(days=1)

            wait_seconds = (target - now).total_seconds()

            print(
                f"Next daily poll: {target.strftime('%Y-%m-%d %H:%M:%S')} UTC "
                f"(4:30 PM IST)"
            )

            await asyncio.sleep(wait_seconds)

            if self.is_closed():
                break

            channel = discord.utils.get(
                self.get_all_channels(),
                name=CHANNEL_NAME
            )

            if channel is None or not hasattr(channel, "send"):
                print(
                    f"ERROR: Could not find #{CHANNEL_NAME}. "
                    "Check the channel name and bot permissions."
                )
                continue

            available_polls = [
                poll for poll in POLLS
                if poll != previous_poll
            ]

            question, answers = random.choice(available_polls)

            try:
                poll_message = discord.Poll(
                    question=question,
                    duration=timedelta(hours=POLL_DURATION_HOURS),
                    multiple=False
                )

                for answer in answers:
                    poll_message.add_answer(text=answer)

                await channel.send(poll=poll_message)

                previous_poll = (question, answers)

                print(f"Daily poll posted successfully: {question}")

            except Exception as error:
                print(f"ERROR posting daily poll: {error}")


bot = PollBot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Daily poll system is running.")
    print("Scheduled time: 4:30 PM IST every day.")


# ==============================
# START BOT
# ==============================

token = os.getenv("DISCORD_TOKEN")

if not token:
    raise RuntimeError(
        "DISCORD_TOKEN environment variable is missing!"
    )

bot.run(token)
```
