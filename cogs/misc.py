import discord
from discord.ext import commands

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game("Type ?help to see a list of commands"))
        print(f"Logged in as {self.client.user}")
        print (f"Connected on {len(self.client.guilds)} servers:")
        for guild in self.client.guilds:
            print(f"{guild.name}\n")

    @commands.command(name = "ping", description = "Pings the bot and displays latency")
    async def ping(self, ctx):
        await ctx.send(f"Pong!{round(self.client.latency * 1000)}ms")

def setup(client):
    client.add_cog(Misc(client))

