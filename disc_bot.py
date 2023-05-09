import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.command()
async def ask(ctx):
    await ctx.send("Please input your response.")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    response = await client.wait_for("message", check=check)
    await ctx.send(f"You said: {response.content}")


# Discord Bot Token: MTEwNTYxNzg0ODk3MTMxNzI1OA.GvKmBv.T-DtHsFGhjnwnBGRhzLvDwZiBbtA85DT7y3A1E

client.run("MTEwNTYxNzg0ODk3MTMxNzI1OA.GvKmBv.T-DtHsFGhjnwnBGRhzLvDwZiBbtA85DT7y3A1E")