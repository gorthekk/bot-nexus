import datetime
import discord
from discord import Embed, app_commands
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

    @commands.Cog.listener()
    async def on_command(self, command):
        if command.author  == self.bot.user:
            return
        else:
            logs_bot = discord.utils.get(command.guild.channels, name="logs_bot")

            event_embed = discord.Embed(title="Command Logged", description="Commande Logger ", color=discord.Color.green())
            event_embed.add_field(name="Command Author:", value=command.author.mention, inline=False)

            await logs_bot.send(embed=event_embed)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            logs_vocal = discord.utils.get(member.guild.channels, name="logs_vocal")
            if not logs_vocal:
                return

            if before.channel is None and after.channel is not None:
                event_embed = discord.Embed(
                    title="🎙️ Voice Join",
                    description=f"{member.mention} a rejoint {after.channel.mention}",
                    color=discord.Color.green()
                )
            
            elif before.channel is not None and after.channel is None:
                event_embed = discord.Embed(
                    title="🎙️ Voice Leave",
                    description=f"{member.mention} a quitté {before.channel.mention}",
                    color=discord.Color.red()
                )

            elif before.channel != after.channel:
                event_embed = discord.Embed(
                    title="🎙️ Voice Move",
                    description=f"{member.mention} a changé de {before.channel.mention} à {after.channel.mention}",
                    color=discord.Color.orange()
                )
            
            event_embed.timestamp = datetime.datetime.utcnow() 
            await logs_vocal.send(embed=event_embed)

        except Exception as e:
            print(f"Error in voice state update: {e}")

        

async def setup(bot):
    await bot.add_cog(Events(bot))