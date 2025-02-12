import discord
from discord.ext import commands
from discord import app_commands

class Kicks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("✓ Kick cog loaded")

    @app_commands.command(
        name="kick",
        description="Kick a member from the server"
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        try:
            if member.top_role >= interaction.user.top_role:
                await interaction.response.send_message(
                    "You cannot kick this member due to role hierarchy!",
                    ephemeral=True
                )
                return

            await member.kick(reason=reason)
            
            embed = discord.Embed(
                title="Member Kicked",
                description=f"{member.mention} has been kicked",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason or "No reason provided")
            embed.add_field(name="Moderator", value=interaction.user.mention)
            
            await interaction.response.send_message(embed=embed)

        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to kick this member!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred: {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Kicks(bot))