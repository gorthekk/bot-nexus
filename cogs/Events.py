import discord
from discord import app_commands
from discord.ext import commands
import random

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name} ({self.bot.user.id})')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        else:

            logs_message = discord.utils.get(message.guild.channels, name="logs_message")

            event_embed = discord.Embed(title="Message Logged",description="Message Logged ",color=discord.Color.random())

            event_embed.add_field(name="Message Author:", value=message.author.mention, inline=False)
            event_embed.add_field(name="Channel Origin:", value=message.channel.mention, inline=False)
            event_embed.add_field(name="Message Content:", value=message.content, inline=False)

            await logs_message.send(embed=event_embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        logs_channel = discord.utils.get(member.guild.channels, name="logs_member")

        event_embed = discord.Embed(title="Arriver Logged",description="Arriver d'un membre Logger ",color=discord.Color.green())

        event_embed.add_field(name="User Joined:", value=member.mention, inline=False)

        await logs_channel.send(embed=event_embed)

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        logs_member = discord.utils.get(member.guild.channels, name="logs_member")

        event_embed = discord.Embed(title="Départ Logged",description="Départ d'un membre Logger ",color=discord.Color.green())

        event_embed.add_field(name="User Leave:", value=member.mention, inline=False)

        await logs_member.send(embed=event_embed)


        

async def setup(bot):
    await bot.add_cog(Events(bot))