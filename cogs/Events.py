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
            
            await logs_vocal.send(embed=event_embed)

        except Exception as e:
            print(f"Error in voice state update: {e}")

    @commands.Cog.listener()
    async def on_member_role_update(self, before, after):
        """Handle role changes for members"""
        try:
            logs_roles = discord.utils.get(after.guild.channels, name="logs_roles")
            if not logs_roles:
                return
    
            # Find added and removed roles
            removed_roles = set(before.roles) - set(after.roles)
            added_roles = set(after.roles) - set(before.roles)
    
            if removed_roles:
                for role in removed_roles:
                    embed = discord.Embed(
                        title="🔴 Role Removed",
                        description=f"Role removed from {before.mention}",
                        color=discord.Color.red(),
                        timestamp=datetime.utcnow()
                    )
                    embed.add_field(name="Role", value=role.mention)
                    await logs_roles.send(embed=embed)
    
            if added_roles:
                for role in added_roles:
                    embed = discord.Embed(
                        title="🟢 Role Added",
                        description=f"Role added to {after.mention}",
                        color=discord.Color.green(),
                        timestamp=datetime.utcnow()
                    )
                    embed.add_field(name="Role", value=role.mention)
                    await logs_roles.send(embed=embed)
    
        except Exception as e:
            print(f"Error in role update: {e}")
    
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """Handle role creation"""
        try:
            logs_roles = discord.utils.get(role.guild.channels, name="logs_roles")
            if logs_roles:
                embed = discord.Embed(
                    title="🟢 Role Created",
                    description=f"New role created",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="Role", value=role.mention)
                embed.add_field(name="Name", value=role.name)
                embed.add_field(name="Color", value=str(role.color))
                await logs_roles.send(embed=embed)
    
        except Exception as e:
            print(f"Error in role create: {e}")
    
    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        """Handle role updates"""
        try:
            logs_roles = discord.utils.get(after.guild.channels, name="logs_roles")
            if logs_roles:
                embed = discord.Embed(
                    title="🔵 Role Updated",
                    description=f"Role modified",
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="Role", value=after.mention)
                
                if before.name != after.name:
                    embed.add_field(name="Name Changed", value=f"From: {before.name}\nTo: {after.name}")
                if before.color != after.color:
                    embed.add_field(name="Color Changed", value=f"From: {before.color}\nTo: {after.color}")
                if before.permissions != after.permissions:
                    embed.add_field(name="Permissions Changed", value="Role permissions were modified")
                    
                await logs_roles.send(embed=embed)
    
        except Exception as e:
            print(f"Error in role update: {e}")
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        """Handle role deletion"""
        try:
            logs_roles = discord.utils.get(role.guild.channels, name="logs_roles")
            if logs_roles:
                embed = discord.Embed(
                    title="🔴 Role Deleted",
                    description=f"Role has been deleted",
                    color=discord.Color.red(),
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="Name", value=role.name)
                embed.add_field(name="Color", value=str(role.color))
                await logs_roles.send(embed=embed)
    
        except Exception as e:
            print(f"Error in role delete: {e}")
    
    @commands.Cog.listener()
    async def on_guild_member_role_add(self, member, role):
        """Handle role addition for members"""
        try:
            logs_roles = discord.utils.get(member.guild.channels, name="logs_roles")
            if logs_roles:
                embed = discord.Embed(
                    title="🟢 Role Added",
                    description=f"Role added to {member.mention}",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="Role", value=role.mention)
                await logs_roles.send(embed=embed)
    
        except Exception as e:
            print(f"Error in role add: {e}")
    
    @commands.Cog.listener()
    async def on_guild_member_role_remove(self, member, role):
        """Handle role removal for members"""
        try:
            logs_roles = discord.utils.get(member.guild.channels, name="logs_roles")
            if logs_roles:
                embed = discord.Embed(
                    title="�� Role Removed",
                    description=f"Role removed from {member.mention}",
                    color=discord.Color.red(),
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="Role", value=role.mention)
                await logs_roles.send(embed=embed)
            
        except Exception as e:
            print(f"Error in role remove: {e}")
        
    
        

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Handle channel deletion"""
        try:
            logs_channel = discord.utils.get(channel.guild.channels, name="logs_channel")
            if logs_channel:
                embed = discord.Embed(
                    title="🔴 Channel Deleted",
                    description="A channel has been deleted",
                    color=discord.Color.red(),
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="Name", value=channel.name, inline=True)
                embed.add_field(name="Type", value=str(channel.type), inline=True)
                embed.add_field(name="Category", value=channel.category.name if channel.category else "None", inline=True)
                await logs_channel.send(embed=embed)
        except Exception as e:
            print(f"Error in channel delete: {e}")
    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """Handle channel creation"""
        try:
            logs_channel = discord.utils.get(channel.guild.channels, name="logs_channel")
            if logs_channel:
                embed = discord.Embed(
                    title="🟢 Channel Created",
                    description="A new channel has been created",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="Name", value=channel.mention, inline=True)
                embed.add_field(name="Type", value=str(channel.type), inline=True)
                embed.add_field(name="Category", value=channel.category.name if channel.category else "None", inline=True)
                await logs_channel.send(embed=embed)
        except Exception as e:
            print(f"Error in channel create: {e}")
    
    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        """Handle channel updates"""
        try:
            logs_channel = discord.utils.get(after.guild.channels, name="logs_channel")
            if logs_channel:
                embed = discord.Embed(
                    title="🔵 Channel Updated",
                    description=f"Changes in {after.mention}",
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow()
                )
                
                # Check what changed
                if before.name != after.name:
                    embed.add_field(name="Name Changed", value=f"From: {before.name}\nTo: {after.name}")
                if before.category != after.category:
                    embed.add_field(
                        name="Category Changed",
                        value=f"From: {before.category.name if before.category else 'None'}\nTo: {after.category.name if after.category else 'None'}"
                    )
                if before.position != after.position:
                    embed.add_field(name="Position Changed", value=f"From: {before.position}\nTo: {after.position}")
                if before.permissions_synced != after.permissions_synced:
                    embed.add_field(name="Permissions Sync Changed", value=f"Now {'synced' if after.permissions_synced else 'not synced'}")
                
                if len(embed.fields) > 0:  # Only send if something changed
                    await logs_channel.send(embed=embed)
                    
        except Exception as e:
            print(f"Error in channel update: {e}")
    
    


    # @tasks.loop(hours=24)
    # async def daily_report(self):
    #     for guild in self.bot.guilds:
    #         try:
    #             # Find logs channel
    #             logs_channel = discord.utils.get(guild.channels, name="logs_server")
    #             if not logs_channel:
    #                 continue

    #             # Create stats embed
    #             embed = discord.Embed(
    #                 title="📊 Daily Server Statistics",
    #                 description=f"Stats for {guild.name}",
    #                 color=discord.Color.blue(),
    #                 timestamp=datetime.utcnow()
    #             )

    #             # Server stats
    #             embed.add_field(
    #                 name="👥 Members",
    #                 value=f"Total: {guild.member_count}\nOnline: {sum(1 for m in guild.members if m.status != discord.Status.offline)}",
    #                 inline=True
    #             )

    #             # Channel stats
    #             text_channels = len(guild.text_channels)
    #             voice_channels = len(guild.voice_channels)
    #             embed.add_field(
    #                 name="📝 Channels",
    #                 value=f"Text: {text_channels}\nVoice: {voice_channels}",
    #                 inline=True
    #             )

    #             # Moderation stats
    #             embed.add_field(
    #                 name="🛡️ Moderation",
    #                 value=f"Kicks: {self.stats['kicks']}\nBans: {self.stats['bans']}\nRole Removes: {self.stats['role_removes']}",
    #                 inline=True
    #             )

    #             # Activity stats
    #             embed.add_field(
    #                 name="📊 Activity",
    #                 value=f"Mentions: {self.stats['mentions']}\nMessages: {self.stats['messages']}",
    #                 inline=True
    #             )

    #             # Reset stats after reporting
    #             self.stats = {key: 0 for key in self.stats}

    #             # Send report with owner mention
    #             owner = guild.owner or await guild.fetch_member(guild.owner_id)
    #             if owner:
    #                 await logs_channel.send(f"{owner.mention}", embed=embed)

    #         except Exception as e:
    #             print(f"Error generating daily report: {e}")

async def setup(bot):
    await bot.add_cog(Events(bot))