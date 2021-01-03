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

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            print("Bot has sent a message")
            return

        if ctx.content.lower() in "hello":
            await ctx.channel.send("hello")

    @commands.command(name = "ping", description = "Pings the bot and displays latency")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    @commands.command(name = "word", description = "says the word flower")
    async def word(self, ctx):
        await ctx.send("flower")

def setup(client):
    client.add_cog(Misc(client))

