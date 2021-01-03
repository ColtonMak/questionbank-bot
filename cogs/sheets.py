import os
import asyncio
import random
import gspread
import discord
from discord.ext import commands
from dotenv import load_dotenv

GSHEET_KEY = os.getenv("GSHEET_KEY")

class Sheets(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.gc = gspread.service_account(filename="credentials.json")
        self.sh = self.gc.open_by_key(GSHEET_KEY)
        self.wks = self.sh.get_worksheet(0)
        self.line = int(self.wks.acell("D1").value)+2
        self.subjects = {
                "\N{Magnet}": "electromagnetism",
                "\N{Telescope}": "astronomy",
                "\N{Earth Globe Americas}": "geography",
                "\N{DNA Double Helix}": "biology",
                "\N{Open Book}": "english"
                }
        self.wksName = ""

    def updateLine(self):
        self.line = int(self.wks.acell("D1").value)+2

    def embedDisplay(self):
        displayStr = ""
        for x, y in self.subjects.items():
            displayStr += f"{x} for {y}\n"
        embed = discord.Embed(
                title = "Select the subject",
                description = displayStr,
                color = discord.Color.blue()
                )
        return embed

    def changeWks(self, arg):
        self.wksName = self.subjects[arg]
        self.wks = self.sh.worksheet(self.wksName)
        self.updateLine()
        print(f"Switched to {self.wksName} sheet")

    def addQuestion(self, question, answer):
        self.wks.update_cell(self.line, 1, question)
        self.wks.update_cell(self.line, 2, answer)
        print(f"Successfully updated line {self.line}")

    def getQuestion(self, line):
        question = self.wks.cell(line, 1).value
        answer = self.wks.cell(line, 2).value
        return (question, answer)

    @commands.command(name = "addEntry",
            description = "Adds an entry to the questionbank in a question and answer format")
    async def addEntry(self, ctx):
        message = await ctx.send(embed=self.embedDisplay())
        for emoji in self.subjects.keys():
            await message.add_reaction(emoji)

        try:
            reaction, user = await self.client.wait_for(
                    "reaction_add",
                    timeout = 60.0,
                    check = lambda reaction, user : user == ctx.author and str(reaction.emoji) in self.subjects.keys()
                    )
            if reaction:
                self.changeWks(str(reaction.emoji))
                await ctx.send(f"Selected {self.wksName}")

        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again")

        try:
            await ctx.send("Enter your question:")
            question = await self.client.wait_for(
                    "message",
                    timeout = 60.0,
                    check = lambda msg : msg.author == ctx.author and msg.channel == ctx.channel
                    )

        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again")

        try:
            await ctx.send("Enter your answer:")
            answer = await self.client.wait_for(
                    "message",
                    timeout = 60.0,
                    check = lambda msg : msg.author == ctx.author and msg.channel == ctx.channel
                    )
            if answer:
                self.addQuestion(question.content, answer.content)
                print(f"Question detected: {question.content}")
                print(f"Answer detected: {answer.content}")
                await ctx.send("Entry successful")
        
        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again")

    @commands.command(name = "question",
            description = "Retrieves a random question from the questionbank for the subject of your choice")
    async def question(self, ctx):
        message = await ctx.send(embed=self.embedDisplay())
        for emoji in self.subjects.keys():
            await message.add_reaction(emoji)

        try:
            reaction, user = await self.client.wait_for(
                    "reaction_add",
                    timeout = 60.0,
                    check = lambda reaction, user : user == ctx.author and str(reaction.emoji) in self.subjects.keys()
                    )
            if reaction:
                self.changeWks(str(reaction.emoji))
                await ctx.send(f"Selected {self.wksName}")

        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again")

        try:
            line = random.randrange(2,self.line-1)
            question, answer = self.getQuestion(line)
            await ctx.send(f"Question: {question}\nAnswer: ||{answer}||")

        except ValueError:
            await ctx.send(f"No questions found for {self.wksName}")

def setup(client):
    client.add_cog(Sheets(client))
