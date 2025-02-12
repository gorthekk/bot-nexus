import discord
from discord.ext import commands
from discord import app_commands

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("✓ Server info cog loaded")

    @commands.command(name="info")
    async def info_prefix(self, ctx):
        """Get information about the server (Prefix: !info)"""
        try:
            embed = discord.Embed(
                title=str(ctx.guild.name),
                description=f'ID: {ctx.guild.id}',
                color=discord.Color.blue()
            )
            
            # Get owner as member object
            owner = ctx.guild.owner or await ctx.guild.fetch_member(ctx.guild.owner_id)
            embed.add_field(name='Owner', value=owner.mention if owner else 'Unknown', inline=True)
            
            embed.add_field(name='Created At', value=ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
            embed.add_field(name='Member Count', value=str(ctx.guild.member_count), inline=True)
            embed.add_field(name='Channels', value=str(len(ctx.guild.channels)), inline=True)
            
            # Fix icon URL access
            if ctx.guild.icon:
                embed.set_thumbnail(url=str(ctx.guild.icon.url))
                
            await ctx.send(embed=embed)
            
        except discord.HTTPException as http_err:
            await ctx.send(f"Discord API error: {http_err}")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
            

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
    print("✓ Server Info cog is ready")