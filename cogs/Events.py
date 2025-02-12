import datetime
import discord
from discord import Embed, app_commands
from discord.ext import commands ,tasks
import random
from datetime import timedelta, datetime
import os
from main import Bot

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.admin_commands = [
            "kick",
            "ban",
            "clear",
        ]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name} ({self.bot.user.id})')

    @commands.Cog.listener()
    async def on_message(self, message):
       #logger dans le channel logs_message les message de mention envers un certain role du serveur en embed 
        if message.mentions:
            logs_channel = discord.utils.get(message.guild.channels, name="logs_staff")

            if logs_channel:
                event_embed = discord.Embed(title="Mention Logged", description="Mention d'un utilisateur Logger ", color=discord.Color.green())

                event_embed.add_field(name="User Mentioned:", value=message.mentions[0].mention, inline=False)
                event_embed.add_field(name="Message:", value=message.content, inline=False)
                event_embed.add_field(name="Channel:", value=message.channel.mention, inline=False)

                await logs_channel.send(embed=event_embed)


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
    async def on_member_kick(self, member, after, before):
        logs_member = discord.utils.get(member.guild.channels, name="logs_btc")

        event_embed = discord.Embed(title="Kick",description="Kick d'un membre  ",color=discord.Color.green())

        event_embed.add_field(name="User Kicked:", value=member.mention, inline=False)
        event_embed.add_field(name="Moderator:", value=before.guild.get_member(before.id).mention, inline=False)
        event_embed.add_field(name="Reason:", value=before.reason or "No reason provided", inline=False)

        await logs_member.send(embed=event_embed)


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

    @commands.Cog.listener()
    async def on_role_remove(self, member, role):
        logs_role = discord.utils.get(member.guild.channels, name="logs_roles")

        if logs_role:
            event_embed = discord.Embed(
                title="��� Role Removed",
                description=f"{member.mention} a supprimé le rôle {role.mention}",
                color=discord.Color.red()
            )
            await logs_role.send(embed=event_embed)
    
    @commands.Cog.listener()
    async def on_role_create(self, role):
        logs_role = discord.utils.get(role.guild.channels, name="logs_roles")
        if logs_role:
            event_embed = discord.Embed(
                title="��� Role Created",
                description=f"Le rôle {role.mention} a été créé",
                color=discord.Color.green()
            )
            await logs_role.send(embed=event_embed)
    
    @commands.Cog.listener()
    async def on_role_update(self, before, after):
        logs_role = discord.utils.get(after.guild.channels, name="logs_roles")
        if logs_role:
            event_embed = discord.Embed(
                title="��� Role Updated",
                description=f"Le rôle {before.mention} a été modifié en {after.mention}",
                color=discord.Color.orange()
            )
            await logs_role.send(embed=event_embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        logs_role = discord.utils.get(role.guild.channels, name="logs_roles")
        if logs_role:
            event_embed = discord.Embed(
                title="��� Role Deleted",
                description=f"Le rôle {role.mention} a été supprimé",
                color=discord.Color.red()
            )
            await logs_role.send(embed=event_embed)
        

    @commands.Cog.listener()
    async def on_channel_create(self, channel):
        logs_channel = discord.utils.get(channel.guild.channels, name="logs_channel")
        if logs_channel:
            event_embed = discord.Embed(
                title="��� Channel Created",
                description=f"Le channel {channel.mention} a été créé",
                color=discord.Color.green()
            )
            await logs_channel.send(embed=event_embed)
    
    @commands.Cog.listener()
    async def on_channel_delete(self, channel):
        logs_channel = discord.utils.get(channel.guild.channels, name="logs_channel")
        if logs_channel:
            event_embed = discord.Embed(
                title="��� Channel Deleted",
                description=f"Le channel {channel.mention} a été supprimé",
                color=discord.Color.red()
            )
            await logs_channel.send(embed=event_embed)
    
    @commands.Cog.listener()
    async def on_channel_update(self, before, after):
        logs_channel = discord.utils.get(after.guild.channels, name="logs_channel")
        if logs_channel:
            event_embed = discord.Embed(
                title="��� Channel Updated",
                description=f"Le channel {before.mention} a été modifié en {after.mention}",
                color=discord.Color.orange()
            )
            await logs_channel.send(embed=event_embed)

    @tasks.loop(hours=24)
    async def daily_report(self):
        for guild in self.bot.guilds:
            try:
                # Find logs channel
                logs_channel = discord.utils.get(guild.channels, name="logs_server")
                if not logs_channel:
                    continue

                # Create stats embed
                embed = discord.Embed(
                    title="📊 Daily Server Statistics",
                    description=f"Stats for {guild.name}",
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow()
                )

                # Server stats
                embed.add_field(
                    name="👥 Members",
                    value=f"Total: {guild.member_count}\nOnline: {sum(1 for m in guild.members if m.status != discord.Status.offline)}",
                    inline=True
                )

                # Channel stats
                text_channels = len(guild.text_channels)
                voice_channels = len(guild.voice_channels)
                embed.add_field(
                    name="📝 Channels",
                    value=f"Text: {text_channels}\nVoice: {voice_channels}",
                    inline=True
                )

                # Moderation stats
                embed.add_field(
                    name="🛡️ Moderation",
                    value=f"Kicks: {self.stats['kicks']}\nBans: {self.stats['bans']}\nRole Removes: {self.stats['role_removes']}",
                    inline=True
                )

                # Activity stats
                embed.add_field(
                    name="📊 Activity",
                    value=f"Mentions: {self.stats['mentions']}\nMessages: {self.stats['messages']}",
                    inline=True
                )

                # Reset stats after reporting
                self.stats = {key: 0 for key in self.stats}

                # Send report with owner mention
                owner = guild.owner or await guild.fetch_member(guild.owner_id)
                if owner:
                    await logs_channel.send(f"{owner.mention}", embed=embed)

            except Exception as e:
                print(f"Error generating daily report: {e}")

    @daily_report.before_loop
    async def before_daily_report(self):
        await self.bot.wait_until_ready()
        # Wait until midnight
        now = datetime.utcnow()
        next_run = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
        await discord.utils.sleep_until(next_run)

    # Event listeners to track stats
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.mentions:
            self.stats['mentions'] += len(message.mentions)
        self.stats['messages'] += 1

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        self.stats['bans'] += 1

    @commands.Cog.listener()
    async def on_member_kick(self, guild, user):
        self.stats['kicks'] += 1

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if len(before.roles) > len(after.roles):
            self.stats['role_removes'] += 1



async def setup(bot):
    await bot.add_cog(Events(bot))