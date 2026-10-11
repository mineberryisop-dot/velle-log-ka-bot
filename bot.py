
import os
import random
import asyncio
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands


# Bot settings
TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_NAME = "poll"

# Daily poll time: 6:00 PM IST = 12:30 UTC
POLL_HOUR_UTC = 12
POLL_MINUTE_UTC = 30


# General polls anyone in the server can answer
POLLS = [
    (
        "What's the most annoying thing ever?",
        ["Slow Wi-Fi", "Low battery", "Being ignored", "Lag 💀"]
    ),
    (
        "Which fictional ability would you choose?",
        ["Teleportation", "Time travel", "Invisibility", "Pause time"]
    ),
    (
        "What's the best way to spend a free day?",
        ["Sleep", "Go outside", "Play games", "Hang out with friends"]
    ),
    (
        "Which school moment is the BEST?",
        ["Free period", "Last bell", "Teacher absent", "Holiday announced"]
    ),
    (
        "Which app would be hardest to give up?",
        ["YouTube", "Discord", "Instagram", "Spotify"]
    ),
    (
        "What ruins a perfectly good day?",
        ["Bad internet", "Unexpected homework", "Plans cancelled", "Phone lag"]
    ),
    (
        "Pick one unlimited freebie.",
        ["Food", "Internet", "Travel", "Games"]
    ),
    (
        "Which snack wins?",
        ["Chips", "Chocolate", "Biscuits", "Instant noodles"]
    ),
    (
        "What type of video do you watch most?",
        ["Memes", "Gaming", "Music", "Random recommendations"]
    ),
    (
        "What's the best kind of weather?",
        ["Rainy", "Cold and cloudy", "Sunny", "Thunderstorms"]
    ),
    (
        "Which notification gets your attention fastest?",
        ["A friend's message", "A server ping", "A sale", "Low battery"]
    ),
    (
        "What's the most difficult thing to do?",
        ["Wake up early", "Sleep early", "Stop scrolling", "Start studying"]
    ),
    (
        "Choose a dream holiday.",
        ["Mountains", "Beach", "Big city", "Stay home comfortably"]
    ),
    (
        "Which game genre is the most fun?",
        ["Action", "Survival", "Racing", "Strategy"]
    ),
    (
        "What's your usual response to 'I'm bored'?",
        ["Open YouTube", "Play a game", "Text someone", "Take a nap"]
    ),
    (
        "What makes a group chat entertaining?",
        ["Memes", "Random conversations", "Friendly arguments", "Chaos 💀"]
    ),
    (
        "Which food could you eat most often?",
        ["Biryani", "Pizza", "Burgers", "Noodles"]
    ),
    (
        "Which is more satisfying?",
        ["Finishing a task", "Winning a game", "Getting good news", "A long weekend"]
    ),
    (
        "Choose one upgrade for your phone.",
        ["Better battery", "More storage", "Faster processor", "Better camera"]
    ),
    (
        "What would you do with an extra hour every day?",
        ["Sleep", "Learn something", "Play games", "Watch videos"]
    ),
    (
        "Which superpower sounds most useful?",
        ["Read minds", "Instant learning", "Teleportation", "Control time"]
    ),
    (
        "What's the worst thing to forget?",
        ["Homework", "Earphones", "A password", "Why you opened an app"]
    ),
    (
        "Pick your ideal gaming session.",
        ["Solo and chill", "With friends", "Competitive", "Trying a new game"]
    ),
    (
        "What's the best kind of humour?",
        ["Memes", "Sarcasm", "Random nonsense", "Inside jokes"]
    ),
    (
        "Which would you rather have?",
        ["Unlimited money", "Unlimited free time", "Perfect memory", "Instant travel"]
    ),
    (
        "What do you usually do when the internet goes down?",
        ["Restart the router", "Use mobile data", "Complain", "Touch grass 😭"]
    ),
    (
        "Which time of day feels best?",
        ["Early morning", "Afternoon", "Evening", "Late night"]
    ),
    (
        "What makes a server feel active?",
        ["Funny conversations", "Daily polls", "Events", "Everyone chatting"]
    ),
    (
        "Which would you choose for a whole week?",
        ["No homework", "No exams", "No early mornings", "Longer holidays"]
    ),
    (
        "What's the most useful everyday skill?",
        ["Cooking", "Fixing tech problems", "Managing money", "Learning quickly"]
    ),
    (
        "What's your preferred way to listen to music?",
        ["Headphones", "Speakers", "Earbuds", "Whatever is available"]
    ),
    (
        "Which is more fun?",
        ["Trying something new", "Getting better at a skill", "Competing", "Relaxing"]
    ),
    (
        "You get ₹5,000 to spend. What comes first?",
        ["Save it", "Buy tech", "Get something fun", "Treat family or friends"]
    ),
    (
        "What is the best kind of online content?",
        ["Funny", "Educational", "Gaming", "Music"]
    ),
    (
        "Which everyday invention is most important?",
        ["Internet", "Smartphone", "Electricity", "Refrigerator"]
    ),
    (
        "What's the best thing about weekends?",
        ["No school", "More sleep", "More gaming", "Time with friends"]
    ),
    (
        "Choose a place to hang out.",
        ["A mall", "A park", "A friend's house", "Online with friends"]
    ),
    (
        "What makes a song memorable?",
        ["Beat", "Melody", "Lyrics", "Overall vibe"]
    ),
    (
        "Which would you rather instantly master?",
        ["A language", "A sport", "A musical instrument", "A school subject"]
    ),
    (
        "What's the funniest type of server moment?",
        ["Random messages", "Unexpected replies", "Funny usernames", "Everyone online at once"]
    ),
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
    print(f"Daily polls will be posted in #{CHANNEL_NAME}.")
    print("Startup test is completely disabled.")


async def post_random_poll():
    global last_poll

    for guild in bot.guilds:
        channel = discord.utils.get(
            guild.text_channels,
            name=CHANNEL_NAME
        )

        if channel is None:
            print(
                f"Could not find #{CHANNEL_NAME} in {guild.name}. "
                "Check the channel name."
            )
            continue

        available_polls = [
            poll for poll in POLLS
            if poll != last_poll
        ]

        if not available_polls:
            available_polls = POLLS

        question, answers = random.choice(available_polls)
        last_poll = (question, answers)

        try:
            poll = discord.Poll(
                question=question,
                duration=timedelta(hours=24),
                multiple=False
            )

            for answer in answers:
                poll.add_answer(text=answer)

            await channel.send(poll=poll)

            print(
                f"Poll posted in #{CHANNEL_NAME} "
                f"in {guild.name}: {question}"
            )

        except Exception as e:
            print(
                f"Could not create poll in {guild.name}: "
                f"{type(e).__name__}: {e}"
            )


async def send_daily_poll():
    await bot.wait_until_ready()

    # No startup test. Only post at the scheduled daily time.
    while not bot.is_closed():
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
            f"Next poll scheduled for {target.isoformat()} "
            f"(UTC). Waiting {wait_seconds / 3600:.2f} hours."
        )

        await asyncio.sleep(wait_seconds)

        if not bot.is_closed():
            await post_random_poll()


async def main():
    async with bot:
        await bot.start(TOKEN)


asyncio.run(main())
