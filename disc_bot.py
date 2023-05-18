import discord
from discord.ext import commands
from dotenv.main import load_dotenv
import os

load_dotenv()
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.command()
async def start(ctx):
    await ctx.send("Please input your response.")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    response = await client.wait_for("message", check=check)
    await ctx.send(f"You said: {response.content}")


client.run(os.environ['DISCORD_API_TOKEN'])