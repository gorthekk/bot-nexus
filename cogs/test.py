import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from datetime import datetime
import humanize

class TestStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stats = {
            "members_joined": 0,
            "members_left": 0,
            "voice_joins": 0,
            "messages_sent": 0,
            "commands_used": 0,
            "role_changes": 0
        }

    @commands.command(name="teststats")
    @commands.has_permissions(administrator=True)
    async def test_daily_stats(self, ctx):
        """Manually trigger daily stats (Admin only)"""
        try:
            guild = ctx.guild
            logs_channel = discord.utils.get(guild.channels, name="logs_server")
            if not logs_channel:
                await ctx.send("❌ Logs channel 'logs_server' not found!")
                return

            # Server Information
            created_time = humanize.naturaltime(guild.created_at)
            
            embed = discord.Embed(
                title=f"📊 Server Statistics for {guild.name}",
                description=f"Server created {created_time}\nID: {guild.id}",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )

            # Member Statistics
            online = sum(1 for m in guild.members if m.status == discord.Status.online)
            idle = sum(1 for m in guild.members if m.status == discord.Status.idle)
            dnd = sum(1 for m in guild.members if m.status == discord.Status.dnd)
            offline = sum(1 for m in guild.members if m.status == discord.Status.offline)
            bots = sum(1 for m in guild.members if m.bot)
            
            embed.add_field(
                name="👥 Members",
                value=f"Total: {guild.member_count}\n"
                      f"Online: {online} 🟢\n"
                      f"Idle: {idle} 🟡\n"
                      f"DND: {dnd} 🔴\n"
                      f"Offline: {offline} ⚫\n"
                      f"Bots: {bots} 🤖\n"
                      f"Humans: {guild.member_count - bots} 👤",
                inline=True
            )

            # Channel Statistics
            categories = len(guild.categories)
            text_channels = len(guild.text_channels)
            voice_channels = len(guild.voice_channels)
            forums = len([c for c in guild.channels if isinstance(c, discord.ForumChannel)])
            
            embed.add_field(
                name="📚 Channels",
                value=f"Categories: {categories} 📑\n"
                      f"Text: {text_channels} 💬\n"
                      f"Voice: {voice_channels} 🎙️\n"
                      f"Forums: {forums} 📋\n"
                      f"Total: {len(guild.channels)} 📊",
                inline=True
            )

            # Voice Activity
            voice_users = sum(1 for m in guild.members if m.voice)
            streaming = sum(1 for m in guild.members if m.voice and m.voice.self_stream)
            
            embed.add_field(
                name="🔊 Voice Status",
                value=f"In Voice: {voice_users} 🎙️\n"
                      f"Streaming: {streaming} 📺\n"
                      f"Active Channels: {sum(1 for vc in guild.voice_channels if len(vc.members) > 0)}/{voice_channels}",
                inline=True
            )

            # Server Features
            features = [f"✓ {feature.replace('_', ' ').title()}" for feature in guild.features]
            if features:
                embed.add_field(
                    name="🌟 Server Features",
                    value="\n".join(features[:6]) + (f"\n*+{len(features)-6} more...*" if len(features) > 6 else ""),
                    inline=True
                )

            # Boost Status
            embed.add_field(
                name="✨ Server Boost",
                value=f"Level: {guild.premium_tier} ⭐\n"
                      f"Boosters: {guild.premium_subscription_count} 🚀\n"
                      f"File Limit: {guild.filesize_limit/1048576:.1f}MB\n"
                      f"Emoji Limit: {guild.emoji_limit} 😄\n"
                      f"Bitrate: {guild.bitrate_limit/1000:.1f}kbps",
                inline=True
            )

            # Set footer and thumbnail
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
            
            embed.set_footer(text=f"Requested by {ctx.author} • {datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')}")

            # Send test report
            await logs_channel.send(embed=embed)
            await ctx.send("✅ Server stats generated in logs_server channel!")

        except Exception as e:
            await ctx.send(f"❌ Error generating test stats: {e}")

async def setup(bot):
    await bot.add_cog(TestStats(bot))