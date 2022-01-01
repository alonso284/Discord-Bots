import discord
from discord.ext import commands
import json


class Score(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")

    # commands
    @commands.command()
    async def score(self, ctx, userOne: discord.Member, userTwo: discord.Member):
        # if userOne == discord.User:
        #     print("workiing")

        if userOne and userTwo:
            # await ctx.send(f"{userOne}, {userTwo}")
            # print(f"{userOne}, {userTwo}")
            with open("scores.json", "w+") as f:
                scoreboard = json.load(f)
                print(scoreboard)

                if scoreboard[userOne.id][userTwo.id]:
                    scoreboard[userOne.id][userTwo.id] = 1
                else:
                    scoreboard[userOne.id][userTwo.id] += 1

                f.json.dump(scoreboard)
        else:
            await ctx.send(f"Error")


def setup(client):
    client.add_cog(Score(client))
